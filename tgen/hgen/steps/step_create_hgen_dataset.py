import uuid
from typing import Set, Tuple, Union

from tgen.common.constants.deliminator_constants import EMPTY_STRING, NEW_LINE
from tgen.common.objects.artifact import Artifact
from tgen.common.objects.trace import Trace
from tgen.common.util.dataframe_util import DataFrameUtil
from tgen.common.util.enum_util import EnumDict
from tgen.data.creators.trace_dataset_creator import TraceDatasetCreator
from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame
from tgen.data.dataframes.layer_dataframe import LayerDataFrame
from tgen.data.dataframes.trace_dataframe import TraceDataFrame
from tgen.data.keys.structure_keys import ArtifactKeys, LayerKeys, TraceKeys
from tgen.data.tdatasets.prompt_dataset import PromptDataset
from tgen.data.tdatasets.trace_dataset import TraceDataset
from tgen.hgen.hgen_args import HGenArgs
from tgen.hgen.hgen_state import HGenState
from tgen.pipeline.abstract_pipeline import AbstractPipelineStep


class CreateHGenDatasetStep(AbstractPipelineStep[HGenArgs, HGenState]):

    def _run(self, args: HGenArgs, state: HGenState) -> None:
        """
        Creates a dataset containing original artifacts, generated upper level artifacts, and trace links between them.
        :param state: The current state of hgen at this point in time
        :param args: The arguments and current state of HGEN.
        :return: None
        """

        _, original_layer_df, original_trace_df = self._get_original_dataframes(state.original_dataset)

        curr_artifact_df = state.selected_artifacts_dataset.artifact_df
        curr_layer_df = CreateHGenDatasetStep._create_layer_df_with_generated_artifacts(args, state, curr_artifact_df)
        curr_trace_df = CreateHGenDatasetStep._create_trace_df_with_generated_artifacts(state, curr_artifact_df, curr_layer_df)

        curr_trace_df = TraceDataFrame.concat(original_trace_df, curr_trace_df) if original_trace_df is not None else curr_trace_df
        curr_layer_df = LayerDataFrame.concat(original_layer_df, curr_layer_df) if original_layer_df is not None else curr_layer_df

        artifact_data_frames = [curr_artifact_df]
        trace_data_frames = [curr_trace_df]
        layer_data_frames = [curr_layer_df]

        if args.add_clusters_as_artifacts:
            cluster_trace_dataset = state.cluster_dataset.trace_dataset
            cluster_artifact_type = cluster_trace_dataset.artifact_df.get_artifact_types()[0]
            artifact2cluster = {a: cluster_id for cluster_id, artifacts in state.seeded_cluster_map.items() for a in artifacts}

            cluster2generated = {}
            for source_artifact in state.original_dataset.artifact_df.to_artifacts():
                source_id = source_artifact[ArtifactKeys.ID]
                artifact_parents = curr_trace_df.get_parents(source_id)
                source_cluster = artifact2cluster[source_id]
                for artifact_parent in artifact_parents:
                    cluster2generated[source_cluster].add(artifact_parent)

            cluster_artifacts = cluster_trace_dataset.artifact_df.to_artifacts()  # TODO: Fix bug where dictionary keys are included as artifacts here
            new_cluster_artifacts = []
            for a in cluster_artifacts:
                new_cluster_artifact = self.create_cluster_artifact(a)
                prev_id = a[ArtifactKeys.ID]
                new_id = new_cluster_artifact[ArtifactKeys.ID]
                if prev_id in cluster2generated:
                    cluster2generated[new_id] = cluster2generated.pop(prev_id)  # rename key
                else:
                    print("oopsies")

                new_cluster_artifacts.append(new_cluster_artifact)
            artifact_df = ArtifactDataFrame(new_cluster_artifacts)
            trace_links = [Trace(source=g_id, target=c_id, label=1, score=1)
                           for c_id, g_ids in cluster2generated.items() for g_id in g_ids]
            trace_df = TraceDataFrame(trace_links)
            layer_df = LayerDataFrame.from_single(source_type=args.target_type, target_type=cluster_artifact_type)

            artifact_data_frames.append(artifact_df)
            trace_data_frames.append(trace_df)
            layer_data_frames.append(layer_df)

        final_artifact_df = ArtifactDataFrame.concat(*artifact_data_frames)
        final_layer_df = LayerDataFrame.concat(*layer_data_frames)
        final_trace_df = TraceDataFrame.concat(*trace_data_frames)

        dataset = PromptDataset(trace_dataset=TraceDataset(final_artifact_df, final_trace_df, final_layer_df),
                                project_summary=args.dataset.project_summary)

        state.final_dataset = dataset

    @staticmethod
    def create_cluster_artifact(cluster_artifact: Artifact):
        curr_id = cluster_artifact[ArtifactKeys.ID].splitlines()
        artifact_id = curr_id[0]
        artifact_content = NEW_LINE.join(curr_id[1:])
        layer_id = cluster_artifact[ArtifactKeys.LAYER_ID]
        new_artifact = Artifact(id=artifact_id, content=artifact_content, layer_id=layer_id, summary=EMPTY_STRING, )
        return new_artifact

    @staticmethod
    def _get_layers_traced(final_artifact_df: ArtifactDataFrame, hgen_state: HGenState) -> Set[str]:
        """
        Gets all layers that were traced to the generated layer.
        :param final_artifact_df: The combined artifact dataframe containing all artifacts (used/generated) in hgen.
        :param hgen_state: The current state of hgen.
        :return: A set of the layer id for all layers that were traced to the generated layer.
        """
        layers_traced = {final_artifact_df.get_artifact(trace[TraceKeys.child_label()])[ArtifactKeys.LAYER_ID]
                         for trace in hgen_state.trace_predictions}
        return layers_traced

    @staticmethod
    def _get_original_dataframes(original_dataset_complete: Union[PromptDataset, TraceDataset]) \
            -> Tuple[ArtifactDataFrame, TraceDataFrame, LayerDataFrame]:
        """
        Gets the dataframes from the original dataset
        :param original_dataset_complete: The original dataset with all layers
        :return: The artifact df and the trace + layer dataframe if they exist
        """
        original_artifact_df = original_dataset_complete.artifact_df
        original_trace_dataset = original_dataset_complete.trace_dataset \
            if isinstance(original_dataset_complete, PromptDataset) else original_dataset_complete
        original_trace_df, original_layer_df = None, None
        if original_trace_dataset:
            original_trace_df = original_trace_dataset.trace_df
            original_layer_df = original_trace_dataset.layer_df
        return original_artifact_df, original_layer_df, original_trace_df

    @staticmethod
    def _create_layer_df_with_generated_artifacts(hgen_args: HGenArgs, hgen_state: HGenState,
                                                  final_artifact_df: ArtifactDataFrame) -> LayerDataFrame:
        """
        Creates a layer dataframe connecting the original lower-level artifacts with the newly generated upper-level artifacts
        :param hgen_args: Arguments to hgen pipeline.
        :param hgen_state: The current state of hgen.
        :param final_artifact_df: The complete artifact dataframe from all artifacts used/created in hgen.
        :return: The dataframe with the new layer ids added.
        """
        layers_traced = CreateHGenDatasetStep._get_layers_traced(final_artifact_df, hgen_state)
        layer_df_map = {}
        for layer_id in layers_traced:
            DataFrameUtil.append(layer_df_map, {LayerKeys.SOURCE_TYPE: layer_id,
                                                LayerKeys.TARGET_TYPE: hgen_args.target_type})
        layer_df = LayerDataFrame(layer_df_map)
        return layer_df

    @staticmethod
    def _create_trace_df_with_generated_artifacts(hgen_state: HGenState,
                                                  artifact_df: ArtifactDataFrame,
                                                  layer_df: LayerDataFrame) -> TraceDataFrame:
        """
        Creates a dataframe of traces including the new trace links between the original lower-level artifacts
        and the newly generated upper-level artifacts
        :param hgen_state: The current state of hgen
        :param artifact_df: The dataframe containing the generated artifacts
        :param layer_df: The dataframe containing the layer mapping between artifacts
        :return: The dataframe containing new and old trace links
        """
        traces = {}
        selected_predictions = hgen_state.selected_predictions
        if selected_predictions:
            for entry in selected_predictions:
                link = EnumDict(entry)
                DataFrameUtil.append(traces, link)

        new_trace_df = TraceDatasetCreator.generate_negative_links(layer_mapping_df=layer_df,
                                                                   artifact_df=artifact_df, trace_df=TraceDataFrame(traces))
        return new_trace_df

    @staticmethod
    def _get_target_layer_id(hgen_args: HGenArgs, original_dataset_complete: PromptDataset) -> str:
        """
        Gets the id of the new target layer
        :param hgen_args: Arguments to hgen pipeline.
        :param original_dataset_complete: Dataset containing original and generated artifacts.
        :return: The id of the new target layer
        """
        layer_id = hgen_args.target_type
        if hgen_args.target_type in original_dataset_complete.artifact_df[ArtifactKeys.LAYER_ID].values:
            layer_id = f"{layer_id}_{uuid.uuid4()}"
            hgen_args.target_type = layer_id
        return layer_id

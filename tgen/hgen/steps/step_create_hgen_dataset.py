import uuid
from typing import Tuple, Union

from tgen.common.util.dataframe_util import DataFrameUtil
from tgen.common.util.enum_util import EnumDict
from tgen.data.creators.trace_dataset_creator import TraceDatasetCreator
from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame
from tgen.data.dataframes.layer_dataframe import LayerDataFrame
from tgen.data.dataframes.trace_dataframe import TraceDataFrame
from tgen.data.keys.structure_keys import ArtifactKeys, LayerKeys
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

        original_artifact_df, original_layer_df, original_trace_df = self._get_original_dataframes(state.original_dataset)

        final_artifact_df = state.all_artifacts_dataset.artifact_df
        new_layer_df = CreateHGenDatasetStep._create_layer_df_with_generated_artifacts(args, args.target_type)
        new_trace_df = CreateHGenDatasetStep._create_trace_df_with_generated_artifacts(state, final_artifact_df, new_layer_df)

        final_trace_df = TraceDataFrame.concat(original_trace_df, new_trace_df) if original_trace_df is not None else new_trace_df
        final_layer_df = LayerDataFrame.concat(original_layer_df, new_layer_df) if original_layer_df is not None else new_layer_df

        dataset = PromptDataset(trace_dataset=TraceDataset(final_artifact_df, final_trace_df, final_layer_df),
                                project_summary=args.dataset.project_summary)

        state.final_dataset = dataset

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
    def _create_layer_df_with_generated_artifacts(hgen_args: HGenArgs, target_layer_id: str) -> LayerDataFrame:
        """
        Creates a layer dataframe connecting the original lower-level artifacts with the newly generated upper-level artifacts
        :param target_layer_id: The id of the new target layer
        :return: The dataframe with the new layer ids added.
        """
        layer_df = LayerDataFrame({LayerKeys.SOURCE_TYPE: [hgen_args.source_layer_id], LayerKeys.TARGET_TYPE: [target_layer_id]})
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
        :param original_dataset_complete: The dataset containing source artifacts
        :return: The id of the new target layer
        """
        layer_id = hgen_args.target_type
        if hgen_args.target_type in original_dataset_complete.artifact_df[ArtifactKeys.LAYER_ID].values:
            layer_id = f"{layer_id}_{uuid.uuid4()}"
            hgen_args.target_type = layer_id
        return layer_id

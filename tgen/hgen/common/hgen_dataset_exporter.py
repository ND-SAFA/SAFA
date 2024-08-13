from typing import Dict, List, Set

from tqdm import tqdm

from common_resources.tools.constants.logging_constants import TQDM_NCOLS
from tgen.common.objects.artifact import Artifact
from tgen.common.objects.trace import Trace
from common_resources.tools.util.dict_util import DictUtil
from common_resources.data.creators.trace_dataset_creator import TraceDatasetCreator
from common_resources.data.dataframes.artifact_dataframe import ArtifactDataFrame
from common_resources.data.dataframes.layer_dataframe import LayerDataFrame
from common_resources.data.dataframes.trace_dataframe import TraceDataFrame
from common_resources.data.keys.structure_keys import ArtifactKeys
from common_resources.data.tdatasets.trace_dataset import TraceDataset
from tgen.hgen.hgen_args import HGenArgs
from tgen.hgen.hgen_state import HGenState


class HGenDatasetBuilder:
    def __init__(self, args: HGenArgs, state: HGenState):
        """
        Creates exporter for pipeline with args and state.
        :param args: Configuration of HGEN pipeline.
        :param state: State of HGEN pipeline.
        """
        self.args = args
        self.state = state
        self._artifact_data_frames: List[ArtifactDataFrame] = []
        self._trace_data_frames = []
        self._layer_data_frames = []

    @staticmethod
    def build(args: HGenArgs, state: HGenState):
        """
        Exports HGEN as a trace dataset from the arguments and state.
        :param args: Configuration of HGEN pipeline to export.
        :param state: State of HGEN pipeline to export.
        :return: Trace dataset containing artifacts, traces, and traced layers.
        """
        builder = HGenDatasetBuilder(args, state)
        builder.add_content()
        trace_dataset = builder.get_trace_dataset()
        trace_dataset.trace_df = TraceDatasetCreator.generate_negative_links(layer_df=trace_dataset.layer_df,
                                                                             trace_df=trace_dataset.trace_df,
                                                                             artifact_df=trace_dataset.artifact_df)
        return trace_dataset

    def add_content(self) -> None:
        """
        Adds source artifacts, generated artifacts, traces between them and optionally clusters and links to them.
        :return: None.
        """
        self.add_original_dataset()
        self.add_generated_content()
        generated_trace_df = self.get_trace_df()

        if self.args.add_seeds_as_artifacts and self.args.get_seed_id(raise_exception=False):
            self.add_seed_data_frames(generated_trace_df)

    def add_original_dataset(self) -> None:
        """
        Adds the content from the original dataset. If ignored, only source artifacts are added.
        :return: None.
        """
        if self.args.export_hgen_artifacts_only:
            self.add_source_artifacts()
        else:
            original_dataset = self.args.dataset
            self._artifact_data_frames.append(self.get_original_artifacts())
            if original_dataset.trace_dataset is not None:
                self._trace_data_frames.append(original_dataset.trace_df)
                self._layer_data_frames.append(original_dataset.layer_df)

    def get_original_artifacts(self):
        """
        Gathers the unique artifacts from all data frames possibly containing source artifacts.
        :return: Artifact data frame containing only unique artifacts.
        """
        datasets = [self.args.dataset.artifact_df, self.state.source_dataset.artifact_df]
        artifact_map = {}
        for dataset_artifact_df in datasets:
            dataset_artifact_map = {a[ArtifactKeys.ID]: a for a in dataset_artifact_df.to_artifacts()}
            artifact_map.update(dataset_artifact_map)
        return ArtifactDataFrame(artifact_map.values())

    def add_source_artifacts(self) -> None:
        """
        Adds the source artifacts to linked artifact data frames.
        :return:None.
        """
        source_artifact_df = self.state.source_dataset.artifact_df
        self._artifact_data_frames.append(source_artifact_df)

    def add_generated_content(self) -> None:
        """
        Adds the artifacts and trace links generated to linked content.
        :return: None.
        """
        generated_artifact_df = self.state.selected_artifacts_dataset.artifact_df.get_artifacts_by_type(self.args.target_type)
        self._artifact_data_frames.append(generated_artifact_df)

        layer_df = LayerDataFrame.from_types(self.args.source_layer_ids, self.args.target_type)
        self._layer_data_frames.append(layer_df)

        trace_df = TraceDataFrame(self.state.selected_predictions)
        self._trace_data_frames.append(trace_df)

    def add_seed_data_frames(self, generated_trace_df: TraceDataFrame) -> None:
        """
        Adds clusters as artifacts and links to generated artifacts through the source artifacts clusters.
        :param generated_trace_df: Links from source artifacts to generated ones. Used to find parents of source artifacts.
        :return: None
        """
        seed_id = self.args.get_seed_id()
        seed_artifact_df = self.state.original_dataset.artifact_df.get_artifacts_by_type(seed_id)
        seed2generated = self.create_seed2generated(self.state, generated_trace_df)

        # Removing the above...
        self.state.cluster_dataset.artifact_df.get_artifacts_by_type(seed_id)
        self._artifact_data_frames.append(seed_artifact_df)

        cluster_trace_df = self.create_cluster_trace_df(seed2generated, seed_artifact_df)
        self._trace_data_frames.append(cluster_trace_df)

        layer_df = LayerDataFrame.from_types(source_types=self.args.target_type, target_types=self.args.get_seed_id())
        self._layer_data_frames.append(layer_df)

    @staticmethod
    def create_seed2generated(state: HGenState, generated_trace_df: TraceDataFrame) -> Dict[str, Set[Artifact]]:
        """
        Creates map of seeds to associated generated artifacts by transitively linking through source artifacts.
        :param state: State of HGen pipeline.
        :param generated_trace_df: TraceDF containing links from source artifacts to generated ones.
        :return: Map of seed id to set of generated artifacts.
        """
        seed2generated = {}
        source_artifacts = state.source_dataset.artifact_df.to_artifacts()
        artifact2seed = {a_id: seed_id for seed_id, artifact_ids in state.seed2artifact_ids.items() for a_id in artifact_ids}

        for source_artifact in tqdm(source_artifacts, ncols=TQDM_NCOLS):
            source_id = source_artifact[ArtifactKeys.ID]
            seed = artifact2seed.get(source_id, None)
            if seed is None:
                continue
            generated_artifacts = generated_trace_df.get_parent_ids(source_id)
            for gen_artifact in generated_artifacts:
                DictUtil.set_or_append_item(seed2generated, seed, gen_artifact, iterable_type=set)

        state
        return seed2generated

    @staticmethod
    def create_cluster_trace_df(cluster2artifacts: Dict[str, Set[Artifact]], seed_df: ArtifactDataFrame) -> TraceDataFrame:
        """
        Creates trace data frame containing links from generated artifacts to seeds.
        :param cluster2artifacts: Map of seeds to associated generated artifacts.
        :param seed_df: The dataframe containing the seed artifacts.
        :return: Dataframe containing links from generated artifacts to seeds.
        """
        content2artifact_id = {a[ArtifactKeys.CONTENT]: a[ArtifactKeys.ID] for a in seed_df.to_artifacts()}
        trace_links = [Trace(source=c_id, target=content2artifact_id[seed_content], label=1, score=1)
                       for seed_content, cluster_ids in cluster2artifacts.items() for c_id in cluster_ids]
        trace_df = TraceDataFrame(trace_links)
        return trace_df

    def get_trace_df(self) -> TraceDataFrame:
        """
        :return: Returns the current trace data frame composed of all those added.
        """
        return TraceDataFrame.concat(*self._trace_data_frames)

    def get_artifact_df(self) -> ArtifactDataFrame:
        """
        :return: Returns the current artifact data frame composed of all those added.
        """
        return ArtifactDataFrame.concat(*self._artifact_data_frames)

    def get_layer_df(self):
        """
        :return: Returns the current layer data frame composed of all those added.
        """
        return LayerDataFrame.concat(*self._layer_data_frames)

    def get_trace_dataset(self) -> TraceDataset:
        """
        :return: Trace dataset containing artifacts, traces, and layers traced.
        """
        return TraceDataset(
            artifact_df=self.get_artifact_df(),
            trace_df=self.get_trace_df(),
            layer_df=self.get_layer_df()
        )

from typing import Dict, List, Set

from tqdm import tqdm

from tgen.common.constants.deliminator_constants import EMPTY_STRING, NEW_LINE
from tgen.common.constants.logging_constants import TQDM_NCOLS
from tgen.common.objects.artifact import Artifact
from tgen.common.objects.trace import Trace
from tgen.common.util.dict_util import DictUtil
from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame
from tgen.data.dataframes.layer_dataframe import LayerDataFrame
from tgen.data.dataframes.trace_dataframe import TraceDataFrame
from tgen.data.keys.structure_keys import ArtifactKeys
from tgen.data.tdatasets.trace_dataset import TraceDataset
from tgen.hgen.hgen_args import HGenArgs
from tgen.hgen.hgen_state import HGenState


class HGenDatasetExporter:
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
    def export(args: HGenArgs, state: HGenState):
        """
        Exports HGEN as a trace dataset from the arguments and state.
        :param args: Configuration of HGEN pipeline to export.
        :param state: State of HGEN pipeline to export.
        :return: Trace dataset containing artifacts, traces, and traced layers.
        """
        exporter = HGenDatasetExporter(args, state)
        exporter.add_content()
        trace_dataset = exporter.get_trace_dataset()
        return trace_dataset

    def add_content(self) -> None:
        """
        Adds source artifacts, generated artifacts, traces between them and optionally clusters and links to them.
        :return: None.
        """
        self.add_original_dataset()
        self.add_generated_content()
        generated_trace_df = self.get_trace_df()

        if self.args.add_clusters_as_artifacts:
            self.add_clusters_data_frames(generated_trace_df)

    def add_original_dataset(self) -> None:
        """
        Adds the content from the original dataset. If ignored, only source artifacts are added.
        :return: None.
        """
        if self.args.export_original_dataset:
            self.add_source_artifacts()
        else:
            original_dataset = self.args.dataset
            self._artifact_data_frames.append(original_dataset.artifact_df)
            self._trace_data_frames.append(original_dataset.trace_df)
            self._layer_data_frames.append(original_dataset.layer_df)

    def add_source_artifacts(self) -> None:
        """
        Adds the source artifacts to linked artifact data frames.
        :return:None.
        """
        source_types = self.args.source_layer_ids
        source_artifact_df = self.state.source_dataset.artifact_df.get_type(source_types)
        self._artifact_data_frames.append(source_artifact_df)

    def add_generated_content(self) -> None:
        """
        Adds the artifacts and trace links generated to linked content.
        :return: None.
        """
        generated_artifact_df = self.state.selected_artifacts_dataset.artifact_df.get_type(self.args.target_type)
        self._artifact_data_frames.append(generated_artifact_df)

        source_types = self.args.source_layer_ids
        layer_df = LayerDataFrame.from_types(source_types, self.args.target_type)
        self._layer_data_frames.append(layer_df)

        generated_traces = self.state.selected_predictions
        trace_df = TraceDataFrame(generated_traces)
        self._trace_data_frames.append(trace_df)

    def add_clusters_data_frames(self, generated_trace_df: TraceDataFrame) -> None:
        """
        Adds clusters as artifacts and links to generated artifacts through the source artifacts clusters.
        :param generated_trace_df: Links from source artifacts to generated ones. Used to find parents of source artifacts.
        :return: None
        """
        seed2generated = HGenDatasetExporter.create_seed2generated(self.state, generated_trace_df)  # seed to generated artifacts.
        seed2artifact = HGenDatasetExporter.create_seed2artifact(self.args, self.state,
                                                                 list(seed2generated.keys()))  # seed to seed artifact

        cluster_artifact_df = ArtifactDataFrame(list(seed2artifact.values()))
        self._artifact_data_frames.append(cluster_artifact_df)

        cluster_trace_df = self.create_cluster_trace_df(seed2generated, seed2artifact)
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
        source_artifacts = state.source_dataset.to_artifacts()
        artifact2seed = {a: cluster_id for cluster_id, artifacts in state.seed2artifacts.items() for a in artifacts}

        for source_artifact in tqdm(source_artifacts, ncols=TQDM_NCOLS):
            source_id = source_artifact[ArtifactKeys.ID]
            seed = artifact2seed.get(source_id, None)
            if seed is None:
                continue
            generated_artifacts = generated_trace_df.get_parents(source_id)
            DictUtil.set_or_append_item(seed2generated, seed, generated_artifacts, iterable_type=set)
        return seed2generated

    @staticmethod
    def create_seed2artifact(args: HGenArgs, state: HGenState, seed_ids: List[str]):
        """
        Creates map of seed to its final artifact.
        :param args: Configuration of HGEN pipeline.
        :param state: State of HGEN pipeline.
        :param seed_ids: List of seeds used.
        :return: Map of seed to artifact for that seed.
        """
        if args.seed_project_summary_section:
            new_seed_map = {seed: HGenDatasetExporter.create_cluster_artifact(seed, args.get_seed_id()) for seed in seed_ids}
        elif args.seed_layer_id:
            seed_artifacts = state.original_dataset.artifact_df.get_type(args.seed_layer_id).to_artifacts()
            content2seed = {a[ArtifactKeys.CONTENT]: a for a in seed_artifacts}  # Content is used to identify each seed.
            new_seed_map = {seed_id: content2seed[seed_id] for seed_id in seed_ids}
        else:
            raise Exception("Unable to identify the seeds to add.")
        return new_seed_map

    @staticmethod
    def create_cluster_trace_df(seed2generated: Dict[str, Set[Artifact]], seed2artifact: Dict[str, Artifact]) -> TraceDataFrame:
        """
        Creates trace data frame containing links from generated artifacts to seeds.
        :param seed2generated: Map of seeds to associated generated artifacts.
        :param seed2artifact: Map of seeds to their artifacts.
        :return: Dataframe containing links from generated artifacts to seeds.
        """
        trace_links = [Trace(source=c_id, target=seed2artifact[seed][ArtifactKeys.ID], label=1, score=1)
                       for seed, cluster_ids in seed2generated.items() for c_id in cluster_ids]
        trace_df = TraceDataFrame(trace_links)
        return trace_df

    @staticmethod
    def create_cluster_artifact(seed_text: str, seed_layer_id: str) -> Artifact:
        """
        Creates artifact for cluster with given content and layer id.
        :param seed_text: The content of the seed.
        :param seed_layer_id: The layer to given the seed artifact.
        :return: Artifact.
        """
        curr_id = seed_text.splitlines()
        artifact_id = curr_id[0]
        artifact_content = NEW_LINE.join(curr_id[1:])
        new_artifact = Artifact(id=artifact_id, content=artifact_content, layer_id=seed_layer_id, summary=EMPTY_STRING)
        return new_artifact

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

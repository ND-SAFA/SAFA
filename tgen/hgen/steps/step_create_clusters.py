from typing import Dict

from tgen.clustering.base.clustering_args import ClusteringArgs
from tgen.clustering.base.clustering_state import ClusteringState
from tgen.clustering.clustering_pipeline import ClusteringPipeline
from tgen.common.constants.clustering_constants import CLUSTERING_SUBDIRECTORY, DEFAULT_SEED_MAX_CLUSTER_SIZE
from tgen.common.constants.deliminator_constants import EMPTY_STRING, NEW_LINE
from tgen.common.constants.hgen_constants import CLUSTER_ARTIFACT_TYPE_PARAM, CLUSTER_MAX_SIZE_PARAM, CLUSTER_SEEDS_PARAM, \
    LARGE_PROJECT, MEDIUM_PROJECT, REDUCTION_FACTORS, SEED_RF_PARAM, SMALL_PROJECT
from tgen.common.constants.ranking_constants import DEFAULT_EMBEDDING_MODEL
from tgen.common.objects.artifact import Artifact
from tgen.common.util.file_util import FileUtil
from tgen.common.util.pipeline_util import nested_pipeline
from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame
from tgen.data.keys.structure_keys import ArtifactKeys
from tgen.embeddings.embeddings_manager import EmbeddingsManager
from tgen.hgen.hgen_args import HGenArgs
from tgen.hgen.hgen_state import HGenState
from tgen.pipeline.abstract_pipeline import AbstractPipelineStep
from tgen.summarizer.summary import SummarySectionKeys


class CreateClustersStep(AbstractPipelineStep[HGenArgs, HGenState]):

    @nested_pipeline(HGenState)
    def _run(self, args: HGenArgs, state: HGenState) -> None:
        """
        Creates clusters from source artifacts to generate new artifacts for each clusters.
        :param args: Arguments to hgen pipeline.
        :param state: Current state of the hgen pipeline.
        :return: None
        """
        if not args.perform_clustering:
            state.embedding_manager = EmbeddingsManager(content_map={}, model_name=DEFAULT_EMBEDDING_MODEL)
            return

        cluster_args = self.create_clustering_args(args, state)
        clustering_pipeline = ClusteringPipeline(cluster_args)
        clustering_pipeline.run()
        self.update_hgen_state(args, state, clustering_pipeline.state)

    @staticmethod
    def update_hgen_state(args: HGenArgs, state: HGenState, cluster_state: ClusteringState) -> None:
        """
        Updates the state of hgen with the result of the clustering pipeline.
        :param args: Arguments to hgen pipeline.
        :param state: The state of the hgen pipeline.
        :param cluster_state: The final state of the clustering pipeline.
        :return: None
        """
        clusters = cluster_state.cluster_artifact_dataset.artifact_df.index.astype(str)  # converting all keys to str bc pd is stupid
        cluster_state.cluster_artifact_dataset.artifact_df.index = clusters
        cluster_map = {str(k): v for k, v in cluster_state.final_cluster_map.items()}

        # Req: Clusters should be added to cluster data frame.
        state.update_total_costs_from_state(cluster_state)
        state.embedding_manager = cluster_state.embedding_manager

        state.cluster_dataset = cluster_state.cluster_artifact_dataset
        state.cluster2artifacts = cluster_map

        if cluster_state.seed2artifacts:
            seed_ids = list(cluster_state.seed2artifacts.keys())
            seed2artifact = {seed: CreateClustersStep.create_cluster_artifact(seed, args.get_seed_id()) for seed in seed_ids}
            new_cluster_artifacts = list(seed2artifact.values())
            seed_rename_map = {seed: a[ArtifactKeys.ID] for seed, a in seed2artifact.items()}

            seed_artifact_df = ArtifactDataFrame(new_cluster_artifacts)
            state.cluster_dataset.artifact_df = ArtifactDataFrame.concat(state.cluster_dataset.artifact_df, seed_artifact_df)
            state.seed2artifacts = {seed_rename_map[s]: artifacts for s, artifacts in cluster_state.seed2artifacts.items()}

    @staticmethod
    def create_clustering_args(args: HGenArgs, state: HGenState) -> ClusteringArgs:
        """
        Creates the configuration of the clustering pipeline basedon the args of the hgen pipeline.
        :param args: The configuration of the hgen pipeline.
        :param state: State of HGEN pipeline.
        :return: The arguments to clustering pipeline.
        """
        uses_seeds = args.seed_project_summary_section or args.seed_layer_id
        seed_kwargs = CreateClustersStep.create_clustering_kwargs(args, state) if uses_seeds else {}
        clustering_export_path = FileUtil.safely_join_paths(args.export_dir, CLUSTERING_SUBDIRECTORY)
        cluster_args = ClusteringArgs(dataset=state.source_dataset, create_dataset=True, export_dir=clustering_export_path,
                                      **seed_kwargs)
        return cluster_args

    @staticmethod
    def create_clustering_kwargs(args: HGenArgs, state: HGenState) -> Dict:
        """
        Creates clustering arguments related to seeding.
        :param args: The arguments to HGEN pipeline.
        :param state: The state of HGEN pipeline.
        :return: Dictionary representing keyword-arguments.
        """
        kwargs = {}
        if args.seed_project_summary_section:
            section_id = args.seed_project_summary_section
            seed_contents = args.dataset.project_summary[section_id][SummarySectionKeys.CHUNKS]
            seed_artifact_type = section_id
            kwargs[SEED_RF_PARAM] = REDUCTION_FACTORS[CreateClustersStep]
        elif args.seed_layer_id:
            seed_artifacts = state.original_dataset.artifact_df.get_type(args.seed_layer_id).to_artifacts()
            seed_contents = [a[ArtifactKeys.CONTENT] for a in seed_artifacts]
            seed_artifact_type = args.seed_layer_id
        else:
            raise Exception("Unable to determine which seeding algorithm to use, received both project section and layer_id.")
        kwargs[CLUSTER_SEEDS_PARAM] = seed_contents
        kwargs[CLUSTER_ARTIFACT_TYPE_PARAM] = seed_artifact_type
        kwargs[CLUSTER_MAX_SIZE_PARAM] = DEFAULT_SEED_MAX_CLUSTER_SIZE
        return kwargs

    @staticmethod
    def get_reduction_factor(args: HGenArgs):
        """
        Calculates the reduction factor based on the number of source artifacts.
        :param args: HGEN args containing source artifacts.
        :return: The reduction factor based on the size of the source artifacts.
        """
        n_sources = len(args.dataset.artifact_df.get_type(args.source_type))
        project_size = CreateClustersStep.get_project_size(n_sources)
        return REDUCTION_FACTORS[project_size]

    @staticmethod
    def get_project_size(n_artifacts: int):
        """
        Returns the size of the project based on the size of the artifacts.
        :param n_artifacts: The number of artifacts in an HGEN run.
        :return: The size of the run.
        """
        if n_artifacts <= 50:
            return SMALL_PROJECT
        elif n_artifacts <= 300:
            return MEDIUM_PROJECT
        else:
            return LARGE_PROJECT

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

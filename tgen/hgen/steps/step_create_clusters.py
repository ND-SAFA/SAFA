from typing import Dict

from tgen.clustering.base.clustering_args import ClusteringArgs
from tgen.clustering.base.clustering_state import ClusteringState
from tgen.clustering.clustering_pipeline import ClusteringPipeline
from tgen.common.constants.ranking_constants import DEFAULT_EMBEDDING_MODEL
from tgen.common.util.file_util import FileUtil
from tgen.common.util.pipeline_util import nested_pipeline
from tgen.data.keys.structure_keys import ArtifactKeys
from tgen.embeddings.embeddings_manager import EmbeddingsManager
from tgen.hgen.hgen_args import HGenArgs
from tgen.hgen.hgen_state import HGenState
from tgen.pipeline.abstract_pipeline import AbstractPipelineStep
from tgen.summarizer.summary import SummarySectionKeys

SEEDS_PARAM = "cluster_seeds"
SEEDS_LAYER_PARAM = "cluster_artifact_type"
SEED_RF_PARAM = "cluster_reduction_factor"


class CreateClustersStep(AbstractPipelineStep[HGenArgs, HGenState]):
    REDUCTION_FACTORS = {"small": 0.5, "medium": 0.3, "big": 0.15}

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

        self.update_hgen_state(state, clustering_pipeline.state)

    @staticmethod
    def create_clustering_args(args: HGenArgs, state: HGenState) -> ClusteringArgs:
        """
        Creates the configuration of the clustering pipeline basedon the args of the hgen pipeline.
        :param args: The configuration of the hgen pipeline.
        :param state: State of HGEN pipeline.
        :return: The arguments to clustering pipeline.
        """
        clustering_kwargs = {}
        if args.seed_project_summary_section or args.seed_layer_id:
            seeding_kwargs = CreateClustersStep.get_seeding_kwargs(args, state)
            state.seeds = seeding_kwargs[SEEDS_PARAM]
            clustering_kwargs.update(seeding_kwargs)
        clustering_export_path = FileUtil.safely_join_paths(args.export_dir, "clustering")
        cluster_args = ClusteringArgs(dataset=state.source_dataset, create_dataset=True, export_dir=clustering_export_path,
                                      cluster_artifact_type=args.seed_layer_id, cluster_max_size=20, **clustering_kwargs)
        return cluster_args

    @staticmethod
    def update_hgen_state(state: HGenState, cluster_state: ClusteringState) -> None:
        """
        Updates the state of hgen with the result of the clustering pipeline.
        :param state: The state of the hgen pipeline.
        :param cluster_state: The final state of the clustering pipeline.
        :return: None
        """
        state.update_total_costs_from_state(cluster_state)
        state.embedding_manager = cluster_state.embedding_manager
        state.seed2artifacts = cluster_state.cluster2artifacts
        state.cluster_dataset = cluster_state.cluster_artifact_dataset
        state.id_to_cluster_artifacts = {str(k): v for k, v in cluster_state.final_cluster_map.items()}
        cluster_state.cluster_artifact_dataset.artifact_df.index = cluster_state.cluster_artifact_dataset.artifact_df.index.astype(str)

    @staticmethod
    def get_seeding_kwargs(args: HGenArgs, state: HGenState) -> Dict:
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
            kwargs[SEED_RF_PARAM] = CreateClustersStep.REDUCTION_FACTORS[CreateClustersStep]
        elif args.seed_layer_id:
            seed_artifacts = state.original_dataset.artifact_df.get_type(args.seed_layer_id).to_artifacts()
            seed_contents = [a[ArtifactKeys.CONTENT] for a in seed_artifacts]
            seed_artifact_type = args.seed_layer_id
        else:
            raise Exception("Unable to determine which seeding algorithm to use, received both project section and layer_id.")
        kwargs[SEEDS_PARAM] = seed_contents
        kwargs[SEEDS_LAYER_PARAM] = seed_artifact_type
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
        return CreateClustersStep.REDUCTION_FACTORS[project_size]

    @staticmethod
    def get_project_size(n_artifacts: int):
        """
        Returns the size of the project based on the size of the artifacts.
        :param n_artifacts: The number of artifacts in an HGEN run.
        :return: The size of the run.
        """
        if n_artifacts <= 50:
            return "small"
        elif n_artifacts <= 300:
            return "medium"
        else:
            return "large"

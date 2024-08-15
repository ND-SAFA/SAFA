from typing import Dict

from common_resources.data.dataframes.artifact_dataframe import ArtifactDataFrame
from common_resources.data.keys.structure_keys import ArtifactKeys
from common_resources.data.objects.artifact import Artifact
from common_resources.data.tdatasets.prompt_dataset import PromptDataset
from common_resources.tools.constants.environment_constants import DEFAULT_EMBEDDING_MODEL
from common_resources.tools.constants.model_constants import USE_NL_SUMMARY_EMBEDDINGS
from common_resources.tools.constants.symbol_constants import EMPTY_STRING
from common_resources.tools.util.file_util import FileUtil
from common_resources.traceability.relationship_manager.embeddings_manager import EmbeddingsManager

from tgen.clustering.base.clustering_args import ClusteringArgs
from tgen.clustering.base.clustering_state import ClusteringState
from tgen.clustering.clustering_pipeline import ClusteringPipeline
from tgen.common.constants.clustering_constants import CLUSTERING_SUBDIRECTORY
from tgen.common.constants.hgen_constants import CLUSTER_ARTIFACT_TYPE_PARAM, CLUSTER_SEEDS_PARAM
from tgen.common.util.clustering_util import ClusteringUtil
from tgen.common.util.pipeline_util import nested_pipeline
from tgen.hgen.common.special_doc_types import DocTypeConstraints
from tgen.hgen.hgen_args import HGenArgs
from tgen.hgen.hgen_state import HGenState
from tgen.pipeline.abstract_pipeline import AbstractPipelineStep


class CreateClustersStep(AbstractPipelineStep[HGenArgs, HGenState]):

    @nested_pipeline(HGenState)
    def _run(self, args: HGenArgs, state: HGenState) -> None:
        """
        Creates clusters from source artifacts to generate new artifacts for each clusters.
        :param args: Arguments to hgen pipeline.
        :param state: Current state of the hgen pipeline.
        :return: None
        """
        if args.check_target_type_constraints(DocTypeConstraints.ONE_TARGET_PER_SOURCE):
            self._create_one_artifact_clusters(state)
            return

        if not args.perform_clustering:
            state.embedding_manager = EmbeddingsManager(content_map={}, model_name=DEFAULT_EMBEDDING_MODEL)
            return

        cluster_args = self.create_clustering_args(args, state)
        clustering_pipeline = ClusteringPipeline(cluster_args)
        clustering_pipeline.run()
        self.update_hgen_state(args, state, clustering_pipeline.state, cluster_args.cluster_max_size)

    @staticmethod
    def _create_one_artifact_clusters(state: HGenState) -> None:
        """
        Creates a cluster for each artifact for a 1-1 relationship.
        :param state: The current hgen state.
        :return: None (updates state).
        """
        state.embedding_manager = EmbeddingsManager(content_map={}, model_name=DEFAULT_EMBEDDING_MODEL)
        n_source_artifacts = len(state.source_dataset.artifact_df.index)
        state.cluster2artifacts = {a_id: [a_id] for a_id in state.source_dataset.artifact_df.index}
        cluster_artifacts = ArtifactDataFrame({ArtifactKeys.ID: [a_id for a_id in state.cluster2artifacts.keys()],
                                               ArtifactKeys.CONTENT: [EMPTY_STRING for _ in range(n_source_artifacts)],
                                               ArtifactKeys.LAYER_ID: [ClusteringArgs.cluster_artifact_type
                                                                       for _ in range(n_source_artifacts)]
                                               })
        state.cluster_dataset = PromptDataset(artifact_df=cluster_artifacts)
        state.cluster2cohesion = {c_id: 1 for c_id in state.cluster2artifacts.keys()}

    @staticmethod
    def update_hgen_state(args: HGenArgs, state: HGenState, cluster_state: ClusteringState, cluster_max_size: int) -> None:
        """
        Updates the state of hgen with the result of the clustering pipeline.
        :param args: Arguments to hgen pipeline.
        :param state: The state of the hgen pipeline.
        :param cluster_state: The final state of the clustering pipeline.
        :param cluster_max_size: The max size allowed for a cluster.
        :return: None
        """
        clusters = cluster_state.cluster_artifact_dataset.artifact_df.index.astype(str)  # converting all keys to str bc pd is stupid
        cluster_state.cluster_artifact_dataset.artifact_df.index = clusters
        cluster_map = ClusteringUtil.convert_cluster_map_to_artifact_format(cluster_state.final_cluster_map)

        # Req: Clusters should be added to cluster data frame.
        state.update_total_costs_from_state(cluster_state)
        state.embedding_manager = cluster_state.embedding_manager

        state.cluster_dataset = cluster_state.cluster_artifact_dataset
        state.cluster2artifacts = cluster_map

        state.cluster2cohesion = {cluster_id: (cluster.avg_pairwise_sim if cluster.avg_pairwise_sim else 1)
                                  for cluster_id, cluster in cluster_state.final_cluster_map.items()}
        if cluster_state.seed2artifacts:
            state.seed2artifact_ids = cluster_state.seed2artifacts
            state.cluster_id2seeds = cluster_state.cluster_id_2seeds

    @staticmethod
    def create_clustering_args(args: HGenArgs, state: HGenState) -> ClusteringArgs:
        """
        Creates the configuration of the clustering pipeline based on the args of the hgen pipeline.
        :param args: The configuration of the hgen pipeline.
        :param state: State of HGEN pipeline.
        :return: The arguments to clustering pipeline.
        """
        uses_seeds = args.seed_project_summary_section or args.seed_layer_id
        seed_kwargs = CreateClustersStep.create_clustering_kwargs(args, state) if uses_seeds else {}
        clustering_export_path = FileUtil.safely_join_paths(args.export_dir, CLUSTERING_SUBDIRECTORY)
        cluster_args = ClusteringArgs(dataset=state.source_dataset, create_dataset=True,
                                      cluster_max_size=args.cluster_max_size,
                                      allow_duplicates_between_clusters=False,
                                      export_dir=clustering_export_path,
                                      add_orphans_to_best_home=not args.allow_orphans, **seed_kwargs)
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
        seed_artifact_type = args.get_seed_id()
        seed_contents = [Artifact.get_summary_or_content(a, use_summary_for_code_only=not USE_NL_SUMMARY_EMBEDDINGS)
                         for a in state.original_dataset.artifact_df.get_artifacts_by_type(seed_artifact_type).to_artifacts()]
        kwargs[CLUSTER_SEEDS_PARAM] = seed_contents
        kwargs[CLUSTER_ARTIFACT_TYPE_PARAM] = seed_artifact_type
        return kwargs

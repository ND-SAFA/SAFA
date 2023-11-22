from tgen.clustering.base.clustering_args import ClusteringArgs
from tgen.clustering.base.clustering_state import ClusteringState
from tgen.clustering.clustering_pipeline import ClusteringPipeline
from tgen.common.constants.ranking_constants import DEFAULT_EMBEDDING_MODEL
from tgen.common.util.file_util import FileUtil
from tgen.data.tdatasets.prompt_dataset import PromptDataset
from tgen.embeddings.embeddings_manager import EmbeddingsManager
from tgen.hgen.hgen_args import HGenArgs
from tgen.hgen.hgen_state import HGenState
from tgen.pipeline.abstract_pipeline import AbstractPipelineStep
from tgen.summarizer.summary import SummarySectionKeys


class CreateClustersStep(AbstractPipelineStep[HGenArgs, HGenState]):

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

        cluster_args = self.create_clustering_args(args, state.source_dataset)
        clustering_pipeline = ClusteringPipeline(cluster_args)
        clustering_pipeline.run()

        self.update_hgen_state(state, clustering_pipeline.state)

    @staticmethod
    def update_hgen_state(state: HGenState, cluster_state: ClusteringState) -> None:
        """
        Updates the state of hgen with the result of the clustering pipeline.
        :param args: The configuration of the HGen pipeline.
        :param state: The state of the hgen pipeline.
        :param cluster_state: The final state of the clustering pipeline.
        :return: None
        """
        state.update_total_costs_from_state(cluster_state)
        state.embedding_manager = cluster_state.embedding_manager
        state.id_to_cluster_artifacts = {str(k): v for k, v in cluster_state.final_cluster_map.items()}
        state.seed2artifacts = cluster_state.seeded_cluster_map
        state.cluster_dataset = cluster_state.cluster_artifact_dataset

    @staticmethod
    def create_clustering_args(args: HGenArgs, source_dataset: PromptDataset) -> ClusteringArgs:
        """
        Creates the configuration of the clustering pipeline basedon the args of the hgen pipeline.
        :param args: The configuration of the hgen pipeline.
        :param source_dataset: Dataset containing source artifacts.
        :return: The arguments to clustering pipeline.
        """
        clustering_pipeline_kwargs = {}
        if args.seed_project_summary_section:
            section_id = args.seed_project_summary_section
            section_chunks = args.dataset.project_summary[section_id][SummarySectionKeys.CHUNKS]
            clustering_pipeline_kwargs["cluster_seeds"] = section_chunks
            clustering_pipeline_kwargs["cluster_artifact_type"] = section_id
            clustering_pipeline_kwargs["cluster_reduction_factor"] = .10
        clustering_export_path = FileUtil.safely_join_paths(args.export_dir, "clustering")
        cluster_args = ClusteringArgs(dataset=source_dataset, create_dataset=True, export_dir=clustering_export_path,
                                      **clustering_pipeline_kwargs)
        return cluster_args

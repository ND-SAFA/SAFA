import numpy as np

from tgen.clustering.base.cluster import Cluster
from tgen.clustering.base.clustering_args import ClusteringArgs
from tgen.clustering.base.clustering_state import ClusteringState
from tgen.common.util.embedding_util import EmbeddingUtil
from tgen.embeddings.embeddings_manager import EmbeddingsManager
from tgen.pipeline.abstract_pipeline import AbstractPipelineStep


class CreateSeededClusters(AbstractPipelineStep[ClusteringArgs, ClusteringState]):
    def _run(self, args: ClusteringArgs, state: ClusteringState) -> None:
        """
        Links artifacts to their nearest seeded cluster.
        :param args: Arguments to clustering pipeline. Starting configuration.
        :param state: Current state of clustering pipeline.
        :return: None
        """
        artifact_ids = list(args.dataset.artifact_df.index)
        embedding_manager: EmbeddingsManager = state.embedding_manager

        artifact_embeddings = embedding_manager.get_embeddings(artifact_ids)

        seed_content_map = {t: t for t in args.cluster_seeds}
        seed_embeddings = embedding_manager.update_or_add_contents(seed_content_map, create_embedding=True)

        similarity_matrix = EmbeddingUtil.calculate_similarities(artifact_embeddings, seed_embeddings)

        cluster_map = {t: [] for t in args.cluster_seeds}
        for i, a_id in enumerate(artifact_ids):
            cluster_similarities = similarity_matrix[i, :]
            closest_cluster_index = np.argmax(cluster_similarities)
            cluster_id = args.cluster_seeds[closest_cluster_index]
            cluster_map[cluster_id].append(a_id)

        cluster_map = {t: Cluster.from_artifacts(artifacts, embedding_manager) for t, artifacts in cluster_map.items()}
        state.final_cluster_map = cluster_map

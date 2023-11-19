from typing import Dict, List

import numpy as np

from tgen.clustering.base.cluster import Cluster
from tgen.clustering.base.clustering_args import ClusteringArgs
from tgen.clustering.base.clustering_state import ClusteringState
from tgen.common.util.embedding_util import EmbeddingUtil
from tgen.embeddings.embeddings_manager import EmbeddingType, EmbeddingsManager
from tgen.pipeline.abstract_pipeline import AbstractPipelineStep


class CreateSeededClusters(AbstractPipelineStep[ClusteringArgs, ClusteringState]):
    def _run(self, args: ClusteringArgs, state: ClusteringState) -> None:
        """
        Links artifacts to their nearest seeded cluster.
        :param args: Arguments to clustering pipeline. Starting configuration.
        :param state: Current state of clustering pipeline.
        :return: None
        """
        seeds = args.cluster_seeds
        artifact_ids = list(args.dataset.artifact_df.index)

        if seeds is None or len(seeds) == 0:
            return

        if len(artifact_ids) == 0:
            raise Exception("Cannot perform seed clustering with no artifacts.")

        embedding_manager: EmbeddingsManager = state.embedding_manager
        cluster_map = self.cluster_with_centroids(embedding_manager, artifact_ids, seeds)
        state.final_cluster_map = {t: Cluster.from_artifacts(artifacts, embedding_manager) for t, artifacts in cluster_map.items()}

    def cluster_with_centroids(self, embedding_manager: EmbeddingsManager, artifact_ids: List[str], centroids: List[str]):
        """
        Clusters artifacts around seeds.
        :param embedding_manager: Used to get artifact and seed embeddings.
        :param artifact_ids: The artifacts to cluster.
        :param centroids: The seeds to cluster around.
        :return:
        """
        artifact_embeddings = embedding_manager.get_embeddings(artifact_ids)
        centroid_embeddings = self.create_embeddings(embedding_manager, centroids)
        similarity_matrix = EmbeddingUtil.calculate_similarities(artifact_embeddings, centroid_embeddings)
        cluster_map = self.assign_clusters_to_artifacts(centroids, artifact_ids, similarity_matrix)
        return cluster_map

    @staticmethod
    def assign_clusters_to_artifacts(centroids: List[str], artifact_ids: List[str], similarity_matrix) -> Dict[str, List[str]]:
        """
        Assigns each artifact to its closest centroid.
        :param centroids: The center of the clusters to assign to artifacts.
        :param artifact_ids: The artifacts to assign to clusters.
        :param similarity_matrix: Similarity between each artifact to each centroid.
        :return: Map of centroid to artifacts it contains.
        """
        cluster_map = {t: [] for t in centroids}
        for i, a_id in enumerate(artifact_ids):
            cluster_similarities = similarity_matrix[i, :]
            closest_cluster_index = np.argmax(cluster_similarities)
            cluster_id = centroids[closest_cluster_index]
            cluster_map[cluster_id].append(a_id)
        return cluster_map

    @staticmethod
    def create_embeddings(embedding_manager: EmbeddingsManager, sentences: List[str]) -> List[EmbeddingType]:
        """
        Creates embeddings for centroids.
        :param embedding_manager: Calculates the embeddings for the sentences.
        :param sentences: The sentences to create embeddings for.
        :return: List of embeddings, for per sentence in the same order as received.
        """
        seed_content_map = {s: s for s in sentences}
        embedding_manager.update_or_add_contents(seed_content_map)
        seed_embeddings = embedding_manager.create_artifact_embeddings(sentences)
        embedding_manager.remove_artifacts(sentences)
        return seed_embeddings

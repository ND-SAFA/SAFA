from typing import Dict, List

import numpy as np

from tgen.clustering.base.clustering_args import ClusteringArgs
from tgen.clustering.base.clustering_state import ClusteringState
from tgen.common.logging.logger_manager import logger
from tgen.common.util.embedding_util import EmbeddingUtil
from tgen.embeddings.embeddings_manager import EmbeddingType, EmbeddingsManager
from tgen.pipeline.abstract_pipeline import AbstractPipelineStep


class CreateBatches(AbstractPipelineStep[ClusteringArgs, ClusteringState]):
    def _run(self, args: ClusteringArgs, state: ClusteringState) -> None:
        """
        Links artifacts to their nearest seeded cluster.
        :param args: Arguments to clustering pipeline. Starting configuration.
        :param state: Current state of clustering pipeline.
        :return: None
        """
        seeds = args.cluster_seeds
        artifact_ids = list(args.dataset.artifact_df.index)
        embedding_manager: EmbeddingsManager = state.embedding_manager
        if len(artifact_ids) == 0:
            raise Exception("Cannot perform seed clustering with no artifacts.")
        if seeds:
            seed2artifacts = self.cluster_around_centroids(embedding_manager, artifact_ids, seeds)
            state.cluster2artifacts = seed2artifacts  # used to link seeds to source artifacts later on.
            artifact_batches = [artifacts for seed, artifacts in seed2artifacts.items() if len(artifacts) > 0]
        else:
            artifact_batches = args.subset_ids if args.subset_ids else [artifact_ids]
        state.artifact_batches = artifact_batches

    @staticmethod
    def cluster_around_centroids(embedding_manager: EmbeddingsManager, artifact_ids: List[str], centroids: List[str]):
        """
        Clusters artifacts around seeds.
        :param embedding_manager: Used to get artifact and seed embeddings.
        :param artifact_ids: The artifacts to cluster.
        :param centroids: The seeds to cluster around.
        :return: Map of centroids to their clustered artifacts.
        """
        artifact_embeddings = embedding_manager.get_embeddings(artifact_ids)
        centroid_embeddings = CreateBatches.create_embeddings(embedding_manager, centroids)
        similarity_matrix = EmbeddingUtil.calculate_similarities(artifact_embeddings, centroid_embeddings)
        cluster_map = CreateBatches.assign_clusters_to_artifacts(centroids, artifact_ids, similarity_matrix)
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
        min_score = np.quantile(similarity_matrix, 0.10)
        upper_threshold = np.quantile(similarity_matrix, 0.95)

        cluster_map = {t: [] for t in centroids}
        n_high_artifacts = 0
        for i, a_id in enumerate(artifact_ids):
            cluster_similarities = similarity_matrix[i, :]

            assigned_clusters_indices = [i for i, score in enumerate(list(cluster_similarities)) if score >= upper_threshold]
            if len(assigned_clusters_indices) == 0:
                closest_cluster_index: int = np.argmax(cluster_similarities)
                closest_cluster_similarity = cluster_similarities[closest_cluster_index]
                if closest_cluster_similarity >= min_score:
                    assigned_clusters_indices.append(closest_cluster_index)
            else:
                n_high_artifacts += 1

            assigned_centroids = [centroids[i] for i in assigned_clusters_indices]

            for assigned_centroid_id in assigned_centroids:
                cluster_map[assigned_centroid_id].append(a_id)
        logger.info(f"# of highly linked artifacts: {n_high_artifacts}")
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

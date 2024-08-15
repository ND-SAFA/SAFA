import math
from typing import Dict, List

import numpy as np
from common_resources.tools.util.np_util import NpUtil
from common_resources.traceability.relationship_manager.embeddings_manager import EmbeddingsManager

from tgen.clustering.base.clustering_args import ClusteringArgs
from tgen.clustering.base.clustering_state import ClusteringState
from tgen.clustering.methods.supported_seed_clustering_methods import SupportedSeedClusteringMethods
from tgen.common.constants.hgen_constants import MIN_SEED_SIMILARITY_QUANTILE, UPPER_SEED_SIMILARITY_QUANTILE
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
        artifact_ids = args.get_artifact_ids()
        embedding_manager: EmbeddingsManager = state.embedding_manager
        if len(artifact_ids) == 0:
            raise Exception("Cannot perform seed clustering with no artifacts.")
        if seeds:
            seed2artifacts = self.cluster_around_centroids(args, embedding_manager, artifact_ids, seeds)
            state.seed2artifacts = seed2artifacts  # used to link seeds to source artifacts later on.
            artifact_batches = [artifacts for seed, artifacts in seed2artifacts.items() if len(artifacts) > 0]
        else:
            artifact_batches = [artifact_ids]
        state.artifact_batches = artifact_batches

    @staticmethod
    def cluster_around_centroids(args: ClusteringArgs, embedding_manager: EmbeddingsManager,
                                 artifact_ids: List[str], centroids: List[str]):
        """
        Clusters artifacts around seeds.
        :param args: Arguments to clustering pipeline. Starting configuration.
        :param embedding_manager: Used to get artifact and seed embeddings.
        :param artifact_ids: The artifacts to cluster.
        :param centroids: The seeds to cluster around.
        :return: Map of centroids to their clustered artifacts.
        """
        CreateBatches.add_sentences_to_embedding_manager(embedding_manager, centroids)
        similarity_matrix = embedding_manager.compare_artifacts(artifact_ids, centroids)
        embedding_manager.remove_artifacts(centroids)
        if args.seed_clustering_method == SupportedSeedClusteringMethods.CENTROID_CHOOSES_ARTIFACTS:
            cluster_map = CreateBatches.assign_centroids_top_artifacts(centroids, artifact_ids, similarity_matrix,
                                                                       max_size=args.cluster_max_size)
        else:
            cluster_map = CreateBatches.assign_clusters_to_artifacts(centroids, artifact_ids, similarity_matrix)
        return cluster_map

    @staticmethod
    def assign_clusters_to_artifacts(centroids: List[str], artifact_ids: List[str], similarity_matrix: np.array,
                                     use_top_centroid_only: bool = False) -> Dict[str, List[str]]:
        """
        Assigns each artifact to its closest centroid.
        :param centroids: The center of the clusters to assign to artifacts.
        :param artifact_ids: The artifacts to assign to clusters.
        :param similarity_matrix: Similarity between each artifact to each centroid.
        :param use_top_centroid_only: If True, artifact is assigned to only the most similar cluster, else all above upper threshold
        :return: Map of centroid to artifacts it contains.
        """
        min_seed_similarity = NpUtil.get_similarity_matrix_percentile(similarity_matrix, MIN_SEED_SIMILARITY_QUANTILE)
        upper_seed_similarity_threshold = NpUtil.get_similarity_matrix_percentile(similarity_matrix, UPPER_SEED_SIMILARITY_QUANTILE)

        cluster_map = {t: [] for t in centroids}
        for i, a_id in enumerate(artifact_ids):
            cluster_similarities = similarity_matrix[i, :]
            assigned_clusters_indices = set({i for i, score in enumerate(list(cluster_similarities)) if
                                             score >= upper_seed_similarity_threshold}) if use_top_centroid_only else set()
            if len(assigned_clusters_indices) == 0:
                closest_cluster_index: int = np.argmax(cluster_similarities)
                closest_cluster_similarity = cluster_similarities[closest_cluster_index]
                if closest_cluster_similarity >= min_seed_similarity:
                    assigned_clusters_indices.add(closest_cluster_index)

            assigned_centroids = [centroids[i] for i in assigned_clusters_indices]

            for assigned_centroid_id in assigned_centroids:
                cluster_map[assigned_centroid_id].append(a_id)
        return cluster_map

    @staticmethod
    def assign_centroids_top_artifacts(centroids: List[str], artifact_ids: List[str], similarity_matrix: np.array,
                                       max_size: int = math.inf) -> Dict[str, List[str]]:
        """
        Assigns each centroid to its closest artifacts.
        :param centroids: The center of the clusters to assign to artifacts.
        :param artifact_ids: The artifacts to assign to clusters.
        :param similarity_matrix: Similarity between each artifact to each centroid.
        :param max_size: If provided, only at most the top n (max_size) artifacts are allowed to be assigned to a centroid
        :return: Map of centroid to artifacts it contains.
        """
        min_seed_similarity = NpUtil.get_similarity_matrix_percentile(similarity_matrix, MIN_SEED_SIMILARITY_QUANTILE)
        upper_seed_similarity_threshold = NpUtil.get_similarity_matrix_percentile(similarity_matrix, UPPER_SEED_SIMILARITY_QUANTILE)

        max_size = min(max_size, len(artifact_ids))
        cluster_map = {}
        for i, c_id in enumerate(centroids):
            artifact_index_and_scores = zip(list(range(len(artifact_ids))), similarity_matrix[:, i])
            ranked_artifact_index_and_scores = sorted(artifact_index_and_scores, reverse=True, key=lambda item: item[1])[:max_size]
            assigned_artifact_indices = {i for i, score in ranked_artifact_index_and_scores
                                         if score >= upper_seed_similarity_threshold}
            if len(assigned_artifact_indices) == 0:
                closest_artifact_index, closest_cluster_similarity = ranked_artifact_index_and_scores[0]
                if closest_cluster_similarity >= min_seed_similarity:
                    assigned_artifact_indices.add(closest_artifact_index)

            cluster_map[c_id] = [artifact_ids[i] for i in assigned_artifact_indices]

        return cluster_map

    @staticmethod
    def add_sentences_to_embedding_manager(embedding_manager: EmbeddingsManager, sentences: List[str]) -> None:
        """
        Creates embeddings for centroids.
        :param embedding_manager: Calculates the embeddings for the sentences.
        :param sentences: The sentences to create embeddings for.
        :return: List of embeddings, for per sentence in the same order as received.
        """
        seed_content_map = {s: s for s in sentences}
        embedding_manager.update_or_add_contents(seed_content_map)
        return

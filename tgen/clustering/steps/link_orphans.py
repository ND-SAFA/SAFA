from typing import List, Set

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from tgen.clustering.base.cluster import Cluster
from tgen.clustering.base.cluster_type import ClusterMapType
from tgen.clustering.base.clustering_args import ClusteringArgs
from tgen.clustering.base.clustering_state import ClusteringState
from tgen.clustering.methods.clustering_algorithm_manager import ClusteringAlgorithmManager
from tgen.clustering.methods.supported_clustering_methods import SupportedClusteringMethods
from tgen.embeddings.embeddings_manager import EmbeddingsManager
from tgen.state.pipeline.abstract_pipeline import AbstractPipelineStep


class LinkOrphans(AbstractPipelineStep[ClusteringArgs, ClusteringState]):
    def _run(self, args: ClusteringArgs, state: ClusteringState) -> None:
        """
        Attempts to link orphans to their best fit cluster, if minimum score is not reached then
        cluster containing singleton artifact is created.
        :param args: The arguments to the clustering pipeline.
        :param state: The current state of the clustering pipeline.
        :return: None, modifications done in place.
        """
        cluster_map: ClusterMapType = state.final_cluster_map
        clusters: List[Cluster] = list(cluster_map.values())

        seen_artifacts = self.collect_unseen_artifacts(clusters)
        all_artifacts = set(state.embedding_manager.get_all_ids())
        orphan_artifact_id_set = all_artifacts.difference(seen_artifacts)

        self.place_orphans_in_homes(cluster_map, orphan_artifact_id_set, state.embedding_manager)
        self.cluster_orphans(cluster_map, orphan_artifact_id_set, state.embedding_manager, args.cluster_reduction_factor)
        for c in cluster_map.values():
            c.calculate_stats(state.embedding_manager)

    @staticmethod
    def cluster_orphans(cluster_map: ClusterMapType, orphan_artifact_id_set: Set[str], embeddings_manager: EmbeddingsManager,
                        reduction_factor: float):
        """
        Attempts to create clusters from the orphan artifacts.
        :param cluster_map: The cluster map to add new clusters to.
        :param orphan_artifact_id_set:Set of orphan artifact ids.
        :param embeddings_manager: Embeddings manager containing orphan artifact embeddings.
        :param reduction_factor: The factor by which to cluster the artifacts.
        :return: None. Cluster map modified in place.
        """
        if len(orphan_artifact_id_set) == 0:
            return
        cluster_manager = ClusteringAlgorithmManager(SupportedClusteringMethods.SPECTRAL)
        clusters = cluster_manager.cluster(embeddings_manager, .4,  # high number to try to group more orphans
                                           subset_ids=list(orphan_artifact_id_set))
        for c in clusters.values():
            if c.avg_similarity >= 0.75:
                next_cluster_index = len(cluster_map)
                cluster_map[next_cluster_index] = c
                for a in c:
                    orphan_artifact_id_set.remove(a)

    @staticmethod
    def collect_unseen_artifacts(clusters: List[Cluster]) -> Set[str]:
        seen_artifacts = set()
        for cluster in clusters:
            for a in cluster.artifact_id_set:
                seen_artifacts.add(a)
        return seen_artifacts

    @staticmethod
    def place_orphans_in_homes(cluster_map: ClusterMapType, orphan_artifacts: Set[str],
                               embeddings_manager: EmbeddingsManager):
        for artifact_id in orphan_artifacts:
            orphan_embedding = embeddings_manager.get_embedding(artifact_id)
            clusters = list(cluster_map.values())  # recalculate each time since new clusters could have been added
            source_matrix = np.matrix([orphan_embedding])
            target_matrix = LinkOrphans.create_centroid_matrix(clusters)
            cluster_similarities = cosine_similarity(source_matrix, target_matrix)[0]
            LinkOrphans.see_if_clusters_want_orphan(artifact_id, clusters, cluster_similarities, embeddings_manager)

    @staticmethod
    def see_if_clusters_want_orphan(artifact_id: str, clusters: List[Cluster],
                                    similarities_to_clusters: List[float], embedding_manager: EmbeddingsManager):
        """
        Places orphan in cluster in which its similarity to the cluster is about the same as the average cluster distance.
        :param artifact_id: The artifact ID of the orphan.
        :param clusters: The clusters to check if want artifact.
        :param similarities_to_clusters: The similarity scores between the orphan embedding and the cluster centroid.
        :param embedding_manager: The embeddings manager allowing clusters to update their stats.
        :return: Whether a cluster has accepted the orphan.
        """
        wanting_clusters = []
        for cluster, similarity_to_cluster in zip(clusters, similarities_to_clusters):
            percent_similar = similarity_to_cluster / cluster.avg_similarity
            print("hi")
            if percent_similar >= 0.75:
                wanting_clusters.append(cluster)

        for c in wanting_clusters:
            c.add_artifact(artifact_id)
            c.calculate_stats(embedding_manager)
        return len(wanting_clusters) > 0

    @staticmethod
    def add_singleton_cluster(a_id: str, cluster_map: ClusterMapType) -> Cluster:
        new_cluster = Cluster()
        new_cluster.add_artifact(a_id)
        next_cluster_index = len(cluster_map)
        cluster_map[next_cluster_index] = new_cluster
        return new_cluster

    @staticmethod
    def create_centroid_matrix(clusters: List[Cluster]) -> np.matrix:
        """
        Creates matrix containing all cluster centroids.
        :param clusters: The clusters whose centroids are stacked.
        :return: Matrix of centroids.
        """
        centroids = [c.centroid.reshape(1, -1)[0] for c in clusters]
        return np.matrix(centroids)

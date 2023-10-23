from typing import List, Set

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from tgen.clustering.base.cluster import Cluster
from tgen.clustering.base.cluster_type import ClusterMapType
from tgen.clustering.base.clustering_args import ClusteringArgs
from tgen.clustering.base.clustering_state import ClusteringState
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
        orphan_artifacts = all_artifacts.difference(seen_artifacts)

        self.place_orphans_in_homes(cluster_map, orphan_artifacts, state.embedding_manager)

        for c in cluster_map.values():
            c.calculate_stats(state.embedding_manager)

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
            cluster_centroids = np.array([c.centroid for c in clusters])
            try:
                source_matrix = np.matrix([orphan_embedding])
                target_matrix =
                cluster_similarities = cosine_similarity([orphan_embedding], np.array(cluster_centroids))[0]
                home_found = LinkOrphans.see_if_clusters_want_orphan(artifact_id, clusters, cluster_similarities, embeddings_manager)
            except Exception as e:
                home_found = False
            if not home_found:
                LinkOrphans.add_singleton_cluster(artifact_id, cluster_map)

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
            artifact_cluster_delta = (cluster.avg_similarity / 1.3) - similarity_to_cluster
            if artifact_cluster_delta < 0:  # found a home
                wanting_clusters.append(cluster)

        add_to_clusters = 0 < len(wanting_clusters) <= 3
        if add_to_clusters:
            for c in wanting_clusters:
                c.add_artifact(artifact_id)
                c.calculate_stats(embedding_manager)
            print("hi")
        return add_to_clusters

    @staticmethod
    def add_singleton_cluster(a_id: str, cluster_map: ClusterMapType):
        new_cluster = Cluster()
        new_cluster.add_artifact(a_id)
        next_cluster_index = len(cluster_map)
        cluster_map[next_cluster_index] = new_cluster

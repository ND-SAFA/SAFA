from typing import List, Set

from tgen.clustering.base.cluster import Cluster
from tgen.clustering.base.cluster_type import ClusterMapType
from tgen.clustering.base.clustering_args import ClusteringArgs
from tgen.clustering.base.clustering_state import ClusteringState
from tgen.clustering.methods.clustering_algorithm_manager import ClusteringAlgorithmManager
from tgen.clustering.methods.supported_clustering_methods import SupportedClusteringMethods
from tgen.embeddings.embeddings_manager import EmbeddingsManager
from tgen.pipeline.abstract_pipeline import AbstractPipelineStep


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

        seen_artifacts = self.collect_seen_artifacts(clusters)
        all_artifacts = set(args.dataset.artifact_df.index)
        orphan_artifact_id_set = all_artifacts.difference(seen_artifacts)

        self.place_orphans_in_homes(clusters, orphan_artifact_id_set, state.embedding_manager)
        self.cluster_orphans(cluster_map, orphan_artifact_id_set, state.embedding_manager, args.min_orphan_similarity)
        for a in orphan_artifact_id_set:
            self.add_singleton_cluster(a, cluster_map, state.embedding_manager)

    @classmethod
    def cluster_orphans(cls, cluster_map: ClusterMapType, orphan_artifact_id_set: Set[str], embeddings_manager: EmbeddingsManager,
                        min_cluster_similarity: float, orphan_cluster_ratio: float = 0.4):
        """
        Attempts to create clusters from the orphan artifacts.
        :param cluster_map: The cluster map to add new clusters to.
        :param orphan_artifact_id_set:Set of orphan artifact ids.
        :param embeddings_manager: Embeddings manager containing orphan artifact embeddings.
        :param orphan_cluster_ratio: The ratio of orphan artifacts to clusters.
        :param min_cluster_similarity: The minimum similarity score for a cluster to be accepted.
        High number default intended to create more clusters to capture sub-groups.
        :return: None. Cluster map modified in place.
        """
        if len(orphan_artifact_id_set) == 0:
            return
        cluster_manager = ClusteringAlgorithmManager(SupportedClusteringMethods.SPECTRAL)
        orphan_cluster_map = cluster_manager.cluster(embeddings_manager, orphan_cluster_ratio, subset_ids=list(orphan_artifact_id_set))
        clusters = [c for c in orphan_cluster_map.values() if c.avg_similarity >= min_cluster_similarity]
        for c in clusters:
            cls.add_cluster(cluster_map, c)
            for a in c:
                orphan_artifact_id_set.remove(a)

    @staticmethod
    def collect_seen_artifacts(clusters: List[Cluster]) -> Set[str]:
        """
        Gathers set of artifacts referenced in clusters.
        :param clusters: List of clusters referencing artifacts in set.
        :return: The set of artifacts referenced.
        """
        seen_artifacts = set()
        for cluster in clusters:
            for a in cluster.artifact_id_set:
                seen_artifacts.add(a)
        return seen_artifacts

    @staticmethod
    def place_orphans_in_homes(clusters: List[Cluster], orphan_artifacts: Set[str], embeddings_manager: EmbeddingsManager) -> None:
        """
        Attempts to add orphans to clusters
        :param clusters: The list of clusters to place orphans into.
        :param orphan_artifacts: List of artifact ids that need clusters.
        :param embeddings_manager: Contains embeddings used to update cluster stats.
        :return:
        """
        for artifact_id in orphan_artifacts:
            accepting_clusters = LinkOrphans.get_clusters_accepting_orphan(artifact_id, clusters, embeddings_manager)
            for c in accepting_clusters:
                c.add_artifact(artifact_id)

    @classmethod
    def get_clusters_accepting_orphan(cls, artifact_id: str, clusters: List[Cluster], embedding_manager: EmbeddingsManager,
                                      avg_similarity_threshold: float = 0.75) -> List[Cluster]:
        """
        Places orphan in cluster in which its similarity to the cluster is about the same as the average cluster distance.
        :param artifact_id: The artifact ID of the orphan.
        :param clusters: The clusters to check if want artifact.
        :param embedding_manager: The embeddings manager allowing clusters to update their stats.
        :param avg_similarity_threshold: The minimum similarity score for an artifact to be considered similar to a cluster.
        :return: The clusters accepting that artifacts.
        """
        wanting_clusters = []
        similarities_to_clusters = [c.similarity_to_neighbors(artifact_id) for c in clusters]
        similarity_score, best_cluster = sorted(zip(similarities_to_clusters, clusters), key=lambda t: t[0], reverse=True)[0]

        if similarity_score >= avg_similarity_threshold:
            wanting_clusters.append(best_cluster)

        return wanting_clusters

    @classmethod
    def add_singleton_cluster(cls, a_id: str, cluster_map: ClusterMapType, embeddings_manager: EmbeddingsManager) -> None:
        """
        Adds singleton cluster containing artifact id to cluster map.ngl
        :param a_id: The artifact to be contained by cluster.
        :param cluster_map: The cluster map to add cluster to.
        :param embeddings_manager: The embeddings manager used to update the cluster stats.
        :return: None. Map updated in place.
        """
        new_cluster = Cluster.from_artifacts([a_id], embeddings_manager)
        cls.add_cluster(cluster_map, new_cluster)

    @staticmethod
    def add_cluster(cluster_map: ClusterMapType, cluster: Cluster) -> None:
        """
        Adds cluster to cluster map at the next index.
        :param cluster_map: The map to add cluster to.
        :param cluster: The cluster to add.
        :return: None. Map modified in place.
        """
        next_cluster_index = len(cluster_map)
        cluster_map[next_cluster_index] = cluster

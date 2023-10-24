from typing import List, Optional, Set

from tgen.clustering.base.cluster import Cluster
from tgen.clustering.base.cluster_type import ClusterMapType, ClusterType
from tgen.common.constants.clustering_constants import DEFAULT_CLUSTERING_MIN_NEW_ARTIFACTS_RATION, DEFAULT_CLUSTER_MIN_VOTES, \
    DEFAULT_CLUSTER_SIMILARITY_THRESHOLD
from tgen.embeddings.embeddings_manager import EmbeddingsManager


class ClusterSelector:
    """
    Responsible for
    """

    def __init__(self, embeddings_manager: EmbeddingsManager, threshold=DEFAULT_CLUSTER_SIMILARITY_THRESHOLD):
        """
        Creates map with similarity threshold.
        :param embeddings_manager: Manages embeddings used to calculate distances between artifacts and clusters.
        :param threshold: The percentage of overlap to which consider sets are the same.
        """
        self.embeddings_manager = embeddings_manager
        self.cluster_map = {}
        self.seen_artifacts = set()
        self.threshold = threshold

    def get_clusters(self, min_votes: int = DEFAULT_CLUSTER_MIN_VOTES) -> ClusterMapType:
        """
        Constructs cluster map from the clusters reaching the minimum number of votes.
        :param min_votes: The minimum number of votes to to include in cluster map.
        :return: Cluster map.
        """
        selected_cluster_ids = [c_id for c_id, cluster in self.cluster_map.items() if cluster.votes >= min_votes]
        selected_cluster_ids = set(selected_cluster_ids)
        cluster_map = {i: self.cluster_map[c_id] for i, c_id in enumerate(selected_cluster_ids)}
        return cluster_map

    def add_all(self, clusters: List[ClusterType]) -> None:
        """
        Adds all clusters to the map.
        :param clusters: List of clusters to add.
        :return: None
        """
        for c in clusters:
            self.add(c)

    def add(self, cluster: Cluster) -> Optional[ClusterType]:
        """
        Adds single cluster to the map.
        :param cluster: The cluster to add.
        :return: Cluster if added, None if cluster is duplicate.
        """
        should_add = self.should_add(cluster)
        if not should_add:
            return
        cluster_id = self.__get_next_cluster_id()
        self.cluster_map[cluster_id] = cluster
        for a in cluster.artifact_ids:
            self.seen_artifacts.add(a)
        return cluster

    def merge_clusters(self, source_cluster: Cluster, new_cluster: Cluster):
        for a_id in new_cluster.artifact_id_set:
            source_cluster.add_artifact(a_id)
            self.seen_artifacts.add(a_id)
        source_cluster.calculate_stats(self.embeddings_manager)

    def should_add(self, cluster: Cluster) -> bool:
        """
        Processes cluster and determines if we should add it to the set.
        :param cluster: The candidate cluster.
        :return: Whether cluster should be added to map.
        """
        contains_new_artifacts = self.contains_new_artifacts(cluster)
        contains_cluster = self.contains_cluster(cluster, add_votes=True)
        did_merge = self.try_merge(cluster)
        if len(cluster) == 1 and not contains_new_artifacts:
            return False
        return (contains_new_artifacts or not contains_cluster) and not did_merge

    def try_merge(self, cluster: Cluster):
        """
        Tries to merge cluster into those similar enough to it.
        :param cluster: The cluster to try to merge.
        :return: Whether the cluster was merged into any others.
        """
        clusters = list(self.cluster_map.values())
        clusters_to_merge_into: List[Cluster] = [c for c in clusters if cluster.similarity_to(c) >= 0.85]
        for source_cluster in clusters_to_merge_into:
            self.merge_clusters(source_cluster, cluster)
        return len(clusters_to_merge_into) > 0

    def contains_cluster(self, other_cluster: ClusterType, add_votes: bool = False) -> bool:
        """
        Calculated whether given cluster is contained within current map.
        :param other_cluster: The cluster to evaluate if contained.
        :param add_votes: Whether to add votes to the clusters where collision is seen.
        :return: True if cluster in map, false otherwise.
        """
        is_hit = False
        cluster_similarities = {}
        for c_id, source_cluster in self.cluster_map.items():
            similarity_to_cluster = self.calculate_intersection(source_cluster.artifact_id_set, other_cluster.artifact_id_set)
            if similarity_to_cluster >= self.threshold:
                is_hit = True
                if add_votes:
                    source_cluster.add_vote()
            cluster_similarities[source_cluster] = similarity_to_cluster
        return is_hit

    def contains_new_artifacts(self, cluster: ClusterType, ratio: float = DEFAULT_CLUSTERING_MIN_NEW_ARTIFACTS_RATION) -> bool:
        """
        Calculates whether cluster has enough or new artifacts to be accepted.
        :param cluster: The cluster to evaluate if it contains enough new artifacts.
        :param ratio: The ratio of new artifacts relative to the cluster size to accept.
        :return: Whether cluster contains a ratio of new artifacts greater or equal to the default value.
        """
        unseen_artifacts = [a for a in cluster if a not in self.seen_artifacts]
        new_artifact_ratio = len(unseen_artifacts) / len(cluster)
        return new_artifact_ratio >= ratio

    def replace(self, cluster: Cluster, new_cluster: Cluster) -> None:
        """
        Replaces first cluster with the new cluster.
        :param cluster: The cluster to replace.
        :param new_cluster: The new cluster to store instead.
        :return: None, new cluster stored in place.
        """
        cluster_ids = [k for k, v in self.cluster_map.items() if v == cluster]
        if len(cluster_ids) > 1:
            raise Exception(f"Found too many clusters matching: {cluster}")
        if len(cluster_ids) == 0:
            raise Exception(f"Could not find cluster: {cluster}")
        cluster_id = cluster_ids[0]
        old_cluster = self.cluster_map[cluster_id]
        self.cluster_map[cluster_id] = new_cluster
        for a in old_cluster:
            self.seen_artifacts.remove(a)
        for a in new_cluster:
            self.seen_artifacts.add(a)
        new_cluster.votes += old_cluster.votes

    def __get_next_cluster_id(self) -> int:
        """
        Gets the id of the next new cluster.
        :return: Next available index.
        """
        return len(self.cluster_map)

    @staticmethod
    def calculate_intersection(source: Set, target: Set) -> float:
        """
        Calculates the percentage the two sets intersect.
        :param source: Set one.
        :param target: Set two.
        :return: The ratio between the number of intersection elements vs the total union.
        """
        c_intersection = source.intersection(target)
        c1_intersection_amount = len(c_intersection) / len(source)
        c2_intersection_amount = len(c_intersection) / len(target)
        avg_intersection_amount = (c1_intersection_amount + c2_intersection_amount) / 2
        return avg_intersection_amount

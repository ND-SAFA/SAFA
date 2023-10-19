from typing import Any, Dict, List, Optional, Set

from tgen.clustering.base.cluster_type import ClusterType

DEFAULT_SIMILARITY_THRESHOLD = 0.85


class UniqueClusterMap:
    """
    Creates methods for incrementally creating a unique cluster map.
    """

    def __init__(self, threshold=DEFAULT_SIMILARITY_THRESHOLD):
        """
        Creates map with similarity threshold.
        :param threshold: The percentage of overlap to which consider sets are the same.
        """
        self.cluster_map = {}
        self.cluster_set_map: Dict[Any, Set] = {}
        self.seen_clusters = set()
        self.threshold = threshold

    def add_all(self, clusters: List[ClusterType]) -> None:
        """
        Adds all clusters to the map.
        :param clusters: List of clusters to add.
        :return: None
        """
        for c in clusters:
            self.add(c)

    def add(self, cluster: ClusterType) -> Optional[ClusterType]:
        """
        Adds single cluster to the map.
        :param cluster: The cluster to add.
        :return: Cluster if added, None if cluster is duplicate.
        """
        if self.contains_cluster(cluster):
            return None
        cluster_id = self.get_next_cluster_id()
        self.cluster_map[cluster_id] = cluster
        self.cluster_set_map[cluster_id] = set(cluster)
        return cluster

    def contains_cluster(self, cluster: ClusterType) -> bool:
        """
        Calculated whether given cluster is contained within current map.
        :param cluster: The cluster to evaluate if contained.
        :return: True if cluster in map, false otherwise.
        """
        cluster_sets = self.cluster_set_map.values()
        target_c_set = set(cluster)
        for c_set in cluster_sets:
            if self.calculate_intersection(c_set, target_c_set) >= self.threshold:
                return True
        return False

    def get_next_cluster_id(self) -> int:
        """
        Gets the id of the next new cluster.
        :return: Next available index.
        """
        return len(self.cluster_map)

    @staticmethod
    def calculate_intersection(c1: Set, c2: Set):
        """
        Calculates the percentage the two sets intersect.
        :param c1: Set one.
        :param c2: Set two.
        :return: The ratio between the number of intersection elements vs the total union.
        """
        c_intersection = c1.intersection(c2)
        c_union = c1.union(c2)
        c_intersection_amount = len(c_intersection) / len(c_union)
        return c_intersection_amount

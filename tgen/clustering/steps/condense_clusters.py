from typing import Dict, List, Set

from typing_extensions import Any

from tgen.clustering.base.cluster_type import ClusterType
from tgen.clustering.base.clustering_args import ClusteringArgs
from tgen.clustering.base.clustering_state import ClusteringState
from tgen.state.pipeline.abstract_pipeline import AbstractPipelineStep


class UniqueClusterMap:
    def __init__(self, threshold=0.85):
        self.cluster_map = {}
        self.cluster_set_map: Dict[Any, Set] = {}
        self.seen_clusters = set()
        self.threshold = threshold

    def add_all(self, clusters: List[ClusterType]):
        for c in clusters:
            self.add(c)

    def add(self, cluster: ClusterType):
        if self.contains_cluster(cluster):
            return None
        cluster_id = self.get_next_cluster_id()
        self.cluster_map[cluster_id] = cluster
        self.cluster_set_map[cluster_id] = set(cluster)

    def contains_cluster(self, cluster: ClusterType) -> bool:
        cluster_sets = self.cluster_set_map.values()
        target_c_set = set(cluster)
        for c_set in cluster_sets:
            if self.calculate_intersection(c_set, target_c_set) >= self.threshold:
                return True
        return False

    def get_next_cluster_id(self) -> int:
        return len(self.cluster_map)

    @staticmethod
    def calculate_intersection(c1: Set, c2: Set):
        c_intersection = c1.intersection(c2)
        c_union = c1.union(c2)
        c_intersection_amount = len(c_intersection) / len(c_union)
        return c_intersection_amount


class CondenseClusters(AbstractPipelineStep[ClusteringArgs, ClusteringState]):
    def _run(self, args: ClusteringArgs, state: ClusteringState, **kwargs) -> None:
        cluster_map = state.multi_method_cluster_map

        clusters = list(cluster_map.values())
        unique_cluster_map = UniqueClusterMap(threshold=args.cluster_intersection_threshold)
        unique_cluster_map.add_all(clusters)

        state.final_cluster_map = unique_cluster_map.cluster_map

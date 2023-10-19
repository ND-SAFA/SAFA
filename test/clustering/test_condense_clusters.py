from unittest import TestCase

from test.clustering.clustering_test_util import ClusteringTestUtil
from tgen.clustering.base.cluster_type import ClusterType
from tgen.clustering.base.clustering_state import ClusteringState
from tgen.clustering.steps.condense_clusters import CondenseClusters


class TestCondenseClusters(TestCase):
    def test_threshold(self):
        """
        Tests that cluster are condensed based on their similarity.
        """
        args = ClusteringTestUtil.create_clustering_args(["hi"])  # artifacts are required, but ignored.
        state = ClusteringState()

        args.cluster_intersection_threshold = 0.75
        c1: ClusterType = ["A", "B", "C", "D"]
        c2: ClusterType = ["A", "B"]
        c3: ClusterType = ["A"]
        state.multi_method_cluster_map = {
            0: c1, 1: ["A", "B", "C"], 2: c2, 3: c3
        }

        CondenseClusters().run(args, state)
        cluster_map = state.final_cluster_map
        ClusteringTestUtil.assert_contains_clusters(cluster_map, [c1, c2, c3])

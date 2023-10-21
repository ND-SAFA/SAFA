from unittest import TestCase

from test.clustering.clustering_test_util import ClusteringTestUtil
from tgen.clustering.base.cluster_type import ClusterType
from tgen.clustering.base.clustering_state import ClusteringState
from tgen.clustering.methods.supported_clustering_methods import SupportedClusteringMethods
from tgen.clustering.steps.condense_clusters import CondenseClusters


class TestCondenseClusters(TestCase):
    def test_threshold(self):
        """
        Tests that cluster are condensed based on their similarity.
        """
        args = ClusteringTestUtil.create_clustering_args(["hi"])  # artifacts are required, but ignored.
        state = ClusteringState()

        args.cluster_min_votes = 1
        args.cluster_intersection_threshold = 0.8
        c1: ClusterType = ["A", "B", "C", "D"]
        c2: ClusterType = ["A", "B"]
        c3: ClusterType = ["A"]
        state.multi_method_cluster_map = {
            SupportedClusteringMethods.KMEANS: {
                0: c1, 1: c2, 2: c3
            },
            SupportedClusteringMethods.AGGLOMERATIVE: {
                0: ["A", "B", "C"]
            }
        }

        CondenseClusters().run(args, state)
        cluster_map = state.final_cluster_map
        ClusteringTestUtil.assert_contains_clusters(cluster_map, [c1, c2, c3])

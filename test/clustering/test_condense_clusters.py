from unittest import TestCase

from test.clustering.clustering_test_util import ClusteringTestUtil
from tgen.clustering.base.cluster import Cluster
from tgen.clustering.base.clustering_state import ClusteringState
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

        embeddings_manager = ClusteringTestUtil.create_embeddings_manager()
        c1: Cluster = Cluster.from_artifacts(["A", "B", "C", "D"], embeddings_manager)
        c2: Cluster = Cluster.from_artifacts(["A", "B"], embeddings_manager)
        c3: Cluster = Cluster.from_artifacts(["A"], embeddings_manager)
        state.batched_cluster_maps = [
            {
                "kmeans0": c1,
                "kmeans2": c2,
                "kmeans3": c3,
                "agglomerative0": Cluster.from_artifacts(["A", "B", "C"], embeddings_manager)
            }
        ]

        CondenseClusters().run(args, state)
        cluster_map = state.final_cluster_map
        ClusteringTestUtil.assert_contains_clusters(cluster_map, [c1, c2, c3])

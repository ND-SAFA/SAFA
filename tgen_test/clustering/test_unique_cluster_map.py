from unittest import TestCase

from tgen_test.clustering.clustering_test_util import ClusteringTestUtil
from tgen.clustering.base.cluster import Cluster
from tgen.clustering.base.cluster_condenser import ClusterCondenser


class TestUniqueClusterMap(TestCase):
    def test_calculate_votes(self):
        """
        Tests that collisions are marked as votes.
        """
        embeddings_manager = ClusteringTestUtil.create_embeddings_manager()
        unique_set_map = ClusterCondenser(embeddings_manager)

        source_cluster = Cluster.from_artifacts(["A", "B"], embeddings_manager)
        collision_cluster = Cluster.from_artifacts(["A", "B"], embeddings_manager)
        unique_set_map.add_all([source_cluster, collision_cluster])

        self.assertTrue(unique_set_map.contains_cluster(collision_cluster))
        self.assertEqual(2, source_cluster.votes)

    def test_intersection_calculation(self):
        """
        Tests that intersection calculation is correctly taking the average of the percentage of intersections.
        """
        set_a = {"A", "B", "C", "D"}  # 25%
        set_b = {"A", "E"}  # 50%
        set_intersection = ClusterCondenser.calculate_intersection(set_a, set_b)
        self.assertEqual(0.375, set_intersection)

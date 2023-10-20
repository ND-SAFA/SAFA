from unittest import TestCase

from tgen.clustering.base.unique_cluster_map import UniqueClusterMap


class TestUniqueClusterMap(TestCase):
    def test_calculate_votes(self):
        """
        Tests that collisions are marked as votes.
        """
        unique_set_map = UniqueClusterMap()
        unique_set_map.add(["A", "B", "C", "D"])
        collision_cluster = ["A", "B"]
        self.assertTrue(unique_set_map.contains_cluster(collision_cluster))
        unique_set_map.add(collision_cluster)
        self.assertEqual(1, unique_set_map.cluster_votes[0])

    def test_intersection_calculation(self):
        """
        Tests that intersection calculation is correctly taking the average of the percentage of intersections.
        """
        set_a = {"A", "B", "C", "D"}
        set_b = {"A", "E"}
        set_intersection = UniqueClusterMap.calculate_intersection(set_a, set_b)
        self.assertEqual(0.375, set_intersection)

from unittest import TestCase

from test.clustering.clustering_test_util import ClusteringTestUtil
from tgen.clustering.base.cluster_type import ClusterMapType
from tgen.clustering.base.clustering_state import ClusteringState
from tgen.clustering.clustering_pipeline import ClusteringPipeline


class TestClusteringPipeline(TestCase):

    def test_use_case(self):
        """
        Tests that simple clustering of sentences results in reasonable clusters.
        """
        args = ClusteringTestUtil.create_default_args(cluster_reduction_factor=0.5, cluster_min_votes=1)
        pipeline: ClusteringPipeline = ClusteringPipeline(args, skip_summarization=True)
        pipeline.run()

        state: ClusteringState = pipeline.state
        clusters: ClusterMapType = state.final_cluster_map

        self.assertEqual(2, len(clusters))
        self.assertIn("A1", clusters[0])
        self.assertIn("A2", clusters[0])
        self.assertIn("A3", clusters[1])
        self.assertIn("A4", clusters[1])

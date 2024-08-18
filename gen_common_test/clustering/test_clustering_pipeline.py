from unittest import TestCase

from gen_common.clustering.base.cluster_type import ClusterMapType
from gen_common.clustering.base.clustering_state import ClusteringState
from gen_common.clustering.clustering_pipeline import ClusteringPipeline
from gen_common_test.clustering.clustering_test_util import ClusteringTestUtil


class TestClusteringPipeline(TestCase):

    def test_use_case(self):
        """
        Tests that simple clustering of sentences results in reasonable clusters.
        """
        args = ClusteringTestUtil.create_default_args(cluster_min_votes=1)
        pipeline: ClusteringPipeline = ClusteringPipeline(args, skip_summarization=True)
        pipeline.run()

        state: ClusteringState = pipeline.state
        clusters: ClusterMapType = state.final_cluster_map

        ClusteringTestUtil.verify_clusters(self, clusters, [["A1", "A2"], ["A3", "A4"]])

    def test_seeds(self):
        """
        Tests ability to cluster around starting sentences.
        """
        seeds = ["animals", "cars"]

        args = ClusteringTestUtil.create_default_args(cluster_seeds=seeds)
        pipeline: ClusteringPipeline = ClusteringPipeline(args, skip_summarization=True)
        pipeline.run()

        state: ClusteringState = pipeline.state
        clusters: ClusterMapType = state.final_cluster_map
        ClusteringTestUtil.verify_clusters(self, clusters, {"animals": ["A1", "A2"], "cars": ["A3", "A4"]})

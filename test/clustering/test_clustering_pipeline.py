from unittest import TestCase, skip

from tgen.clustering.clustering_args import ClusteringArgs
from tgen.clustering.clustering_pipeline import ClusteringPipeline


class TestClusteringPipeline(TestCase):
    @skip
    def test_use_case(self):
        """
        TODO:
        :return:
        """
        args = ClusteringArgs()
        pipeline = ClusteringPipeline(args)
        pipeline.run()

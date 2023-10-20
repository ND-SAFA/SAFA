from unittest import TestCase

from test.clustering.clustering_test_util import ClusteringTestUtil
from tgen.clustering.base.clustering_state import ClusteringState
from tgen.clustering.methods.supported_cluster_methods import SupportedClusterMethods
from tgen.clustering.steps.cluster_embeddings import ClusterEmbeddings
from tgen.clustering.steps.create_embeddings import CreateEmbeddings
from tgen.common.constants.clustering_constants import DEFAULT_TESTING_CLUSTERING_METHODS


class TestClusterEmbeddings(TestCase):
    def test_use_case(self):
        """
        Tests that multiple algorithms are used to create clusters for artifacts.
        """
        artifact_map = {
            "A1": "Doggies are really cute.",
            "A2": "Car goes vroom.",
            "A3": "Fire trucks are really loud.",
            "A4": "Dogs pee on fire hydrants."
        }
        artifacts = list(artifact_map.values())

        state = ClusteringState()
        args = ClusteringTestUtil.create_clustering_args(artifacts)

        CreateEmbeddings().run(args, state)
        ClusterEmbeddings().run(args, state)

        method_cluster_map = state.multi_method_cluster_map
        for clustering_method_name in DEFAULT_TESTING_CLUSTERING_METHODS:
            supported_clustering_method = SupportedClusterMethods[clustering_method_name]
            method_name = supported_clustering_method.name
            self.assertIn(method_name, method_cluster_map)
            c_id = f"{method_name}0"
            self.assertIn(c_id, method_cluster_map[method_name])

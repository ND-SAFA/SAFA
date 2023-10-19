from unittest import TestCase

from test.clustering.clustering_test_util import ClusteringTestUtil
from tgen.clustering.base.clustering_state import ClusteringState
from tgen.clustering.methods.cluster_method import ClusterMethod
from tgen.clustering.steps.cluster_embeddings import ClusterEmbeddings
from tgen.clustering.steps.create_embeddings import CreateEmbeddings
from tgen.common.constants.hugging_face_constants import SMALL_EMBEDDING_MODEL


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

        embeddings_map = CreateEmbeddings.create_embeddings_map(artifact_map, SMALL_EMBEDDING_MODEL)
        state.embedding_map = embeddings_map

        ClusterEmbeddings().run(args, state)

        cluster_map = state.multi_method_cluster_map
        for c in ClusterMethod:
            c_id = f"{c.value().get_id()}0"
            self.assertIn(c_id, cluster_map)

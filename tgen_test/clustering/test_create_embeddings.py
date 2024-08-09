from unittest import TestCase

from tgen_test.clustering.clustering_test_util import ClusteringTestUtil
from tgen.clustering.base.clustering_state import ClusteringState
from tgen.clustering.steps.create_embeddings import CreateEmbeddings


class TestCreateEmbeddings(TestCase):
    def test_use_case(self):
        """
        Tests that embeddings are calculated and correctly stored with their corresponding artifact.
        """
        a1 = "I have a dog."
        a2 = "Cats are cool too."

        args = ClusteringTestUtil.create_clustering_args([a1, a2])
        state = ClusteringState()

        CreateEmbeddings().run(args, state)
        embedding_map = state.embedding_manager.get_current_embeddings()

        self.assertEqual(2, len(embedding_map))
        ClusteringTestUtil.assert_embeddings_equals("A1 " + a1, embedding_map["A1"])
        ClusteringTestUtil.assert_embeddings_equals("A2 " + a2, embedding_map["A2"])

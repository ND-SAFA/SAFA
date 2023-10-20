import os
from unittest import mock
from unittest.mock import MagicMock

import numpy as np
from sentence_transformers.SentenceTransformer import SentenceTransformer

from tgen.common.util.yaml_util import YamlUtil
from tgen.data.keys.structure_keys import ArtifactKeys
from tgen.embeddings.embeddings_manager import EmbeddingsManager
from tgen.testres.base_tests.base_test import BaseTest
from tgen.testres.paths.paths import TEST_OUTPUT_DIR
from tgen.testres.testprojects.safa_test_project import SafaTestProject


class TestEmbeddingManager(BaseTest):

    @mock.patch.object(SentenceTransformer, "encode")
    def test_create_embedding_map(self, encode_mock: MagicMock):
        content_map = {artifact[ArtifactKeys.ID.value]: artifact[ArtifactKeys.CONTENT.value]
                       for artifact in SafaTestProject.get_artifact_entries()}
        embeddings = [[i for i in range(j, j + 3)] for j in range(len(content_map))]
        embedding_arrays = [np.asarray(emb) for emb in embeddings]
        encode_mock.side_effect = [embedding_arrays[:3], embedding_arrays[3:]]

        embedding_manager = EmbeddingsManager(content_map=content_map, model_name="sentence-transformers/all-MiniLM-L6-v2")

        embeddings = embedding_manager.create_embedding_map(subset_ids=["s1", "s2", "s3"])
        self.assertEqual(len(embeddings), 3)

        embeddings = embedding_manager.create_embedding_map()
        self.assertEqual(len(embeddings), len(content_map))
        self.assertEqual(encode_mock.call_count, 2)  # each artifact encoded only once

        original_embeddings = embedding_manager.get_current_embeddings()
        path = os.path.join(TEST_OUTPUT_DIR, "test.yaml")
        key = "embedding_manager"
        YamlUtil.write({key: embedding_manager}, path)  # test to_yaml
        loaded_manager: EmbeddingsManager = YamlUtil.read(path)[key]  # test from_yaml
        loaded_embeddings = loaded_manager.get_current_embeddings()
        self.assertEqual(len(loaded_embeddings), len(original_embeddings))
        for a_id, embedding in original_embeddings.items():
            self.assertIn(a_id, loaded_embeddings)
            self.assertEqual(list(embedding), list(loaded_embeddings[a_id]))

        self.assertFalse(loaded_manager.embeddings_need_saved(os.path.join(TEST_OUTPUT_DIR, key)))
        loaded_manager.update_or_add_content("s1", "something new")
        self.assertTrue(loaded_manager.embeddings_need_saved(os.path.join(TEST_OUTPUT_DIR, key)))

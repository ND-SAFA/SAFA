import os
from unittest import mock
from unittest.mock import MagicMock

import numpy as np
from sentence_transformers.SentenceTransformer import SentenceTransformer

from tgen.common.constants.hugging_face_constants import SMALL_EMBEDDING_MODEL
from tgen.common.util.list_util import ListUtil
from tgen.common.util.yaml_util import YamlUtil
from tgen.data.keys.structure_keys import ArtifactKeys
from tgen.relationship_manager.embeddings_manager import EmbeddingsManager
from tgen.testres.base_tests.base_test import BaseTest
from tgen.testres.paths.paths import TEST_OUTPUT_DIR
from tgen.testres.testprojects.safa_test_project import SafaTestProject


class TestEmbeddingManager(BaseTest):

    @mock.patch.object(SentenceTransformer, "encode")
    def test_create_embedding_map(self, encode_mock: MagicMock):
        content_map, embedding_manager = self.create_test_embedding_manager(encode_mock)

        embeddings = embedding_manager.create_embedding_map(subset_ids=["s1", "s2", "s3"])
        self.assertEqual(len(embeddings), 3)

        embeddings = embedding_manager.create_embedding_map()
        self.assertEqual(len(embeddings), len(content_map))
        self.assertEqual(encode_mock.call_count, 2)  # each artifact encoded only once

    def test_saving_and_loading_from_yaml(self):
        content_map, embedding_manager = self.create_test_embedding_manager()
        original_embeddings = embedding_manager.create_embedding_map()
        path = os.path.join(TEST_OUTPUT_DIR, "test.yaml")
        key = "embedding_manager"
        YamlUtil.write({key: embedding_manager}, path)  # test to_yaml
        loaded_manager: EmbeddingsManager = YamlUtil.read(path)[key]  # test from_yaml
        loaded_embeddings = loaded_manager.get_current_embeddings()
        self.assertEqual(len(loaded_embeddings), len(original_embeddings))
        for a_id, embedding in original_embeddings.items():
            self.assertIn(a_id, loaded_embeddings)
            self.assertEqual(list(embedding), list(loaded_embeddings[a_id]))
        self.assertFalse(loaded_manager.need_saved(os.path.join(TEST_OUTPUT_DIR, key)))
        loaded_manager.update_or_add_content("s1", "something new")
        self.assertTrue(loaded_manager.need_saved(os.path.join(TEST_OUTPUT_DIR, key)))

    @mock.patch.object(SentenceTransformer, "encode")
    def test_update_or_add_contents(self, encode_mock: MagicMock):
        content_map, embedding_manager = self.create_test_embedding_manager(encode_mock)
        original_embeddings = embedding_manager.create_embedding_map(["s1", "s2"])
        original_embeddings = {k: ListUtil.convert_numpy_array_to_native_types(v) for k, v in original_embeddings.items()}
        new_content_map = {"s1": "new content", "new_art": "some content", "s2": content_map["s2"]}
        embedding_manager.update_or_add_contents(new_content_map)
        new_embeddings = embedding_manager.create_embedding_map(subset_ids=new_content_map.keys())
        new_embeddings = {k: ListUtil.convert_numpy_array_to_native_types(v) for k, v in new_embeddings.items()}
        self.assertEqual(original_embeddings["s2"], new_embeddings["s2"])
        self.assertNotEqual(original_embeddings["s1"], new_embeddings["s1"])
        self.assertIn("new_art", new_embeddings)

        for key, val in new_content_map.items():
            self.assertEqual(embedding_manager.get_content(key), val)

    def test_merge(self):
        content_map1, embedding_manager1 = self.create_test_embedding_manager()
        embedding_manager1.create_embedding_map()
        content_map2 = {"new_artifact1": "a1",
                        "new_artifact2": "a2"}
        embedding_manager2 = EmbeddingsManager(content_map=content_map2,
                                               model_name=SMALL_EMBEDDING_MODEL)
        embedding_manager2.create_embedding_map(subset_ids=["new_artifact1"])
        embedding_manager1.merge(embedding_manager2)
        content_map1.update(content_map2)
        for a_id in content_map1.keys():
            if a_id == "new_artifact2":
                self.assertNotIn(a_id, embedding_manager1.get_current_embeddings())
            else:
                self.assertIn(a_id, embedding_manager1.get_current_embeddings())
            self.assertEqual(embedding_manager1.get_content(a_id), content_map1[a_id])

    def create_test_embedding_manager(self, encode_mock=None):
        content_map = {artifact[ArtifactKeys.ID.value]: artifact[ArtifactKeys.CONTENT.value]
                       for artifact in SafaTestProject.get_artifact_entries()}
        embeddings = [[i for i in range(j, j + 3)] for j in range(len(content_map))]
        embedding_arrays = [np.asarray(emb) for emb in embeddings]
        if encode_mock:
            encode_mock.side_effect = [embedding_arrays[:3], embedding_arrays[3:]]
        embedding_manager = EmbeddingsManager(content_map=content_map, model_name=SMALL_EMBEDDING_MODEL)
        return content_map, embedding_manager

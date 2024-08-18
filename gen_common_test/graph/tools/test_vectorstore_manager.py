from unittest import mock
from unittest.mock import MagicMock

from langchain_community.vectorstores.chroma import Chroma

from gen_common.data.dataframes.artifact_dataframe import ArtifactDataFrame
from gen_common.data.keys.structure_keys import ArtifactKeys
from gen_common.data.objects.artifact import Artifact
from gen_common.data.tdatasets.prompt_dataset import PromptDataset
from gen_common.graph.io.graph_args import GraphArgs
from gen_common.graph.llm_tools.vector_store_manager import VectorStoreManager
from gen_common.constants.hugging_face_constants import SMALL_EMBEDDING_MODEL
from gen_common_test.base.tests.base_test import BaseTest
from gen_common_test.testprojects.safa_test_project import SafaTestProject


class TestVectorStoreManager(BaseTest):
    NEW_ARTIFACT_ID = "new_artifact"
    NEW_ARTIFACT_CONTENT = "The cat in the hat sat on a mat"

    @mock.patch.object(Chroma, "add_documents")
    def test_update_or_add_contents(self, add_docs_mock: MagicMock):
        vectorstore_manager = self.create_test_vectorstore_manager()
        new_artifact_id = "new_art"
        same_artifact_id = "s2"
        new_content_map = {
            "s1": "new content",
            new_artifact_id: "some content",
            same_artifact_id: vectorstore_manager.get_content("s2")
        }
        # VP - Verify that artifact is not yet in database
        self.assertFalse(vectorstore_manager.contains("new_art"))

        # Step - Add new artifacts.
        updated_ids = vectorstore_manager.update_or_add_contents(new_content_map)

        # VP - Verify that updated ids match those specified.
        update_mock_call = add_docs_mock.mock_calls[1]
        update_mock_call_artifact_ids = [d.id for d in update_mock_call.args[0]]
        self.assertListEqual(updated_ids, update_mock_call_artifact_ids)

        # Verify that only artifact's with new content got updated.
        self.assertIn("s1", updated_ids)
        self.assertIn(new_artifact_id, updated_ids)
        self.assertNotIn(same_artifact_id, updated_ids)

        # Verify that all artifact's still exist
        for key in new_content_map.keys():
            self.assertTrue(vectorstore_manager.contains(key))

        # Step - Perform a another update
        new_artifact_id2 = "another_art"
        vectorstore_manager.update_or_add_content(artifact=Artifact(id=new_artifact_id2, content="more content"))
        self.assertTrue(vectorstore_manager.contains(new_artifact_id2))

    def test_search(self):
        vectorstore_manager = self.create_test_vectorstore_manager()

        vectorstore_manager.update_or_add_content(self.NEW_ARTIFACT_ID, self.NEW_ARTIFACT_CONTENT)
        query = "cat"
        # search with threshold
        docs = vectorstore_manager.search(query, threshold=0.8, include_scores=False)
        self.assertEqual(docs[query][0].metadata["id"], self.NEW_ARTIFACT_ID)
        docs = vectorstore_manager.search(query, threshold=0.8, include_scores=True)
        self.assertEqual(docs[query][0][0].metadata["id"], self.NEW_ARTIFACT_ID)
        self.assertEqual(docs[query][0][1], 1)

        # search with max return
        docs = vectorstore_manager.search(query, max_returned=3, threshold=None, include_scores=True)
        self.assertEqual(docs[query][0][0].metadata["id"], self.NEW_ARTIFACT_ID)
        self.assertIsInstance(docs[query][0][1], float)
        self.assertEqual(len(docs[query]), 3)
        docs = vectorstore_manager.search(query, max_returned=3, threshold=None, include_scores=False)
        self.assertEqual(docs[query][0].metadata["id"], self.NEW_ARTIFACT_ID)
        self.assertEqual(len(docs[query]), 3)

        # update content and search
        vectorstore_manager.update_or_add_content("s2", "A lion is also a cat")
        docs = vectorstore_manager.search(query, threshold=0.8, include_scores=False)
        self.assertIn("s2", [doc.metadata["id"] for doc in docs[query]])

    def test_add_context_from_args(self):
        args = self.get_args()

        vectorstore_manager1 = self.create_test_vectorstore_manager()
        vectorstore_manager1.add_context_from_args(args)

        vectorstore_manager2 = VectorStoreManager.from_args(args)
        for vectorstore_manager in [vectorstore_manager1, vectorstore_manager2]:
            self.assertIn(self.NEW_ARTIFACT_ID, vectorstore_manager.id_to_artifacts)
            self.assertTrue(vectorstore_manager.contains(self.NEW_ARTIFACT_ID))

    def test_create_from_content(self):
        vectorstore_manager = VectorStoreManager.create_from_content([self.NEW_ARTIFACT_CONTENT, "other_content"])
        self.assertTrue(vectorstore_manager.contains(self.NEW_ARTIFACT_CONTENT))
        self.assertEqual(len(vectorstore_manager), 2)

    def test_remove_artifacts(self):
        artifacts2remove = ["s1", "s2"]
        vectorstore_manager = self.create_test_vectorstore_manager()
        vectorstore_manager.remove_artifacts(artifacts2remove)
        for a_id in artifacts2remove:
            self.assertFalse(vectorstore_manager.contains(a_id))

    def test_compare_artifacts(self):
        vectorstore_manager = self.create_test_vectorstore_manager()
        score = vectorstore_manager.compare_artifact("s1", "s2")
        self.assertGreaterEqual(score, 0.5)

    def get_args(self):
        dataset = PromptDataset(artifact_df=ArtifactDataFrame({ArtifactKeys.ID: [self.NEW_ARTIFACT_ID],
                                                               ArtifactKeys.CONTENT: [self.NEW_ARTIFACT_CONTENT],
                                                               ArtifactKeys.LAYER_ID: ["dr_suess"]}))
        return GraphArgs(dataset=dataset)

    def create_test_vectorstore_manager(self):
        artifacts = SafaTestProject.get_artifact_entries()
        artifact_dict = {key.value: [artifact[key] for artifact in artifacts]
                         for key in [ArtifactKeys.ID, ArtifactKeys.CONTENT, ArtifactKeys.LAYER_ID]}
        embedding_manager = VectorStoreManager(artifact_df=ArtifactDataFrame(artifact_dict), model_name=SMALL_EMBEDDING_MODEL)
        return embedding_manager

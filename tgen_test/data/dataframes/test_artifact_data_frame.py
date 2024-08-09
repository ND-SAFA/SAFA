from tgen.common.constants.deliminator_constants import PERIOD
from tgen.common.objects.artifact import Artifact
from tgen.common.objects.chunk import Chunk
from tgen.common.util.dict_util import DictUtil
from tgen.common.util.enum_util import EnumDict
from tgen.common.util.list_util import ListUtil
from tgen.data.chunkers.sentence_chunker import SentenceChunker
from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame
from tgen.data.keys.structure_keys import ArtifactKeys
from tgen.testres.base_tests.base_test import BaseTest


class TestArtifactDataFrame(BaseTest):

    def test_add_artifact(self):
        df = self.get_artifact_data_frame()
        artifact = df.add_artifact("s3", "body3", 2)
        self.assert_artifact(artifact, "s3", "body3", 2)

        df_empty = ArtifactDataFrame()
        artifact = df_empty.add_artifact("s3", "body3", 2)
        self.assert_artifact(artifact, "s3", "body3", 2)

    def test_get_artifact(self):
        df = self.get_artifact_data_frame()
        artifact = df.get_artifact("s1")
        self.assert_artifact(artifact, "s1", "body1", "0")

        artifact_does_not_exist = df.get_artifact("s3")
        self.assertIsNone(artifact_does_not_exist)

    def assert_artifact(self, artifact: EnumDict, id_, body, layer_id):
        self.assertEqual(artifact[ArtifactKeys.ID], id_)
        self.assertEqual(artifact[ArtifactKeys.CONTENT], body)
        self.assertEqual(artifact[ArtifactKeys.LAYER_ID], layer_id)

    def test_is_summarized(self):
        no_summaries = self.get_artifact_data_frame()
        self.assertFalse(no_summaries.is_summarized())

        some_summaries = no_summaries
        some_summaries[ArtifactKeys.SUMMARY] = [("summary" if i.endswith(".py") else None) for i in some_summaries.index]
        self.assertFalse(some_summaries.is_summarized())

        self.assertTrue(some_summaries.is_summarized(code_or_above_limit_only=True))
        some_summaries.add_artifact("s3", "body3", layer_id="1")  # add a none code artifact to the code layer
        self.assertFalse(some_summaries.is_summarized(layer_ids="1"))  # the entire layer is no longer summarized
        self.assertTrue(some_summaries.is_summarized(code_or_above_limit_only=True))  # but the code part of the layer is

        all_summarized = some_summaries
        all_summarized.update_values(ArtifactKeys.SUMMARY, list(all_summarized.index), ["summary" for i in all_summarized.index])
        self.assertTrue(all_summarized.is_summarized())

    def test_chunk(self):
        a_dataframe = self.get_artifact_data_frame()
        unchunked_id, unchunked_content = "unchunked", "One sentence. Two sentence. This is multiple sentences."
        chunked_id, chunked_content = "chunked", "This one is already chunked. But it has two sentences."
        ignored_id, ignored_content = "ignored", "This has multiple sentences. But we are going to exclude it from ids."

        a_dataframe.add_artifact(unchunked_id, unchunked_content)
        a_dataframe.add_artifact(chunked_id, chunked_content, chunks=["Chunk1", "Chunk2"])
        a_dataframe.add_artifact(ignored_id, ignored_content)
        artifact_ids = {a_id for a_id in a_dataframe.index if a_id != "ignored"}

        chunk_map = a_dataframe.chunk(SentenceChunker(), artifact_ids=artifact_ids,
                                      unchunked_only=False)
        expected_chunked_artifacts = {unchunked_id: unchunked_content, chunked_id: chunked_content}
        self._assert_chunking(chunk_map, expected_chunked_artifacts)
        chunk_map = a_dataframe.chunk(SentenceChunker(), unchunked_only=True)
        expected_chunked_artifacts = {ignored_id: ignored_content}
        self._assert_chunking(chunk_map, expected_chunked_artifacts)
        for chunk_id in expected_chunked_artifacts:
            self.assertEqual(a_dataframe.get_artifact_from_chunk_id(chunk_id, id_only=True), ignored_id)
            self.assertEqual(a_dataframe.get_artifact_from_chunk_id(chunk_id, id_only=False)[ArtifactKeys.CONTENT], ignored_content)
        self.assertEqual(a_dataframe.get_artifact_from_chunk_id(ignored_id, id_only=True), ignored_id)
        chunk_id = Chunk.get_chunk_id(ignored_id, 1)
        self.assertEqual(a_dataframe.get_chunk_by_id(chunk_id), chunk_map[chunk_id])
        self.assertIsNone(a_dataframe.get_chunk_by_id(Chunk.get_chunk_id(ignored_id, 5)))
        self.assertIsNone(a_dataframe.get_chunk_by_id(Chunk.get_chunk_id("unknown", 0)))

    def test_update_or_add_values(self):
        a_dataframe = self.get_artifact_data_frame()
        existing_artifact_id = a_dataframe.index.to_list()[0]
        new_artifact_id = "new_id"
        updated_artifact = Artifact(id=existing_artifact_id, content="updated content", layer_id="updated layer")
        new_artifact = Artifact(id=new_artifact_id, content="new content", layer_id="new layer")
        updated_df = ArtifactDataFrame.update_or_add_values(a_dataframe, [updated_artifact, new_artifact])
        self.assertEqual(updated_df.get_row(existing_artifact_id)[ArtifactKeys.CONTENT], updated_artifact[ArtifactKeys.CONTENT])
        self.assertNotEqual(a_dataframe.get_row(existing_artifact_id)[ArtifactKeys.CONTENT], updated_artifact[ArtifactKeys.CONTENT])
        self.assertEqual(updated_df.get_row(new_artifact_id)[ArtifactKeys.CONTENT], new_artifact[ArtifactKeys.CONTENT])
        self.assertNotIn(new_artifact_id, a_dataframe)

    def _assert_chunking(self, chunk_map, expected_chunked_artifacts):
        chunks = {}
        for chunk_id, chunk in chunk_map.items():
            success = False
            for a_id in expected_chunked_artifacts:
                if chunk_id.startswith(a_id):
                    DictUtil.set_or_append_item(chunks, a_id, (chunk_id, chunk))
                    success = True
            self.assertTrue(success)
        for a_id, chunks in chunks.items():
            sorted_chunks = ListUtil.unzip(sorted(chunks, key=lambda item: item[0][-1]),
                                           item_index=1)
            original_content = expected_chunked_artifacts[a_id]
            self.assertEqual(len(chunks), original_content.count(PERIOD))
            self.assertEqual(". ".join(sorted_chunks) + PERIOD, original_content)

    def get_artifact_data_frame(self):
        return ArtifactDataFrame({ArtifactKeys.ID: ["s1", "s2.py"], ArtifactKeys.CONTENT: ["body1", "body2"],
                                  ArtifactKeys.LAYER_ID: ["0", "1"]})

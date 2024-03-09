from tgen.common.util.enum_util import EnumDict
from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame
from tgen.data.keys.structure_keys import ArtifactKeys
from tgen.testres.base_tests.base_test import BaseTest


class TestArtifacteDataFrame(BaseTest):

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

    def get_artifact_data_frame(self):
        return ArtifactDataFrame({ArtifactKeys.ID: ["s1", "s2.py"], ArtifactKeys.CONTENT: ["body1", "body2"],
                                  ArtifactKeys.LAYER_ID: ["0", "1"]})

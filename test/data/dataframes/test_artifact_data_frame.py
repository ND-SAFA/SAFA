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
        self.assert_artifact(artifact, "s1", "body1", 0)

        artifact_does_not_exist = df.get_artifact("s3")
        self.assertIsNone(artifact_does_not_exist)

    def assert_artifact(self, artifact: EnumDict, id_, body, layer_id):
        self.assertEqual(artifact[ArtifactKeys.ID], id_)
        self.assertEqual(artifact[ArtifactKeys.CONTENT], body)
        self.assertEqual(artifact[ArtifactKeys.LAYER_ID], layer_id)

    def get_artifact_data_frame(self):
        return ArtifactDataFrame({ArtifactKeys.ID: ["s1", "s2"], ArtifactKeys.CONTENT: ["body1", "body2"],
                                  ArtifactKeys.LAYER_ID: [0, 1]})

from typing import NamedTuple

from data.dataframes.artifact_dataframe import ArtifactDataFrame, ArtifactKeys
from testres.base_test import BaseTest
from util.enum_util import EnumDict


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
        self.assertEquals(artifact[ArtifactKeys.ID], id_)
        self.assertEquals(artifact[ArtifactKeys.CONTENT], body)
        self.assertEquals(artifact[ArtifactKeys.LAYER_ID], layer_id)

    def get_artifact_data_frame(self):
        return ArtifactDataFrame({ArtifactKeys.ID: ["s1", "s2"], ArtifactKeys.CONTENT: ["body1", "body2"],
                                  ArtifactKeys.LAYER_ID: [0, 1]})

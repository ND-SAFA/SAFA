from test.base_test import BaseTest
from data.data_objects.artifact import Artifact


def fake_method(text):
    return {"feature_name": text}


class TestArtifact(BaseTest):
    TOKEN = "token"

    def test_get_feature(self):
        test_artifact = self.get_test_artifact()
        feature = test_artifact.get_feature(fake_method)
        self.assertEquals(feature["feature_name"], self.TOKEN)

    def get_test_artifact(self):
        return Artifact("id", self.TOKEN)

from test.base_test import BaseTest
from trace.data.artifact import Artifact


def fake_method(text):
    return {"feature_name": text}


class TestArtifact(BaseTest):
    TOKEN = "token"

    def test_get_feature(self):
        test_artifact = self.get_test_artifact()
        feature = test_artifact.get_feature()
        self.assertEquals(feature["feature_name"], self.TOKEN)

        # second time calling get_feature should not call feature_func again
        test_artifact.token = "changed_token"
        feature = test_artifact.get_feature()
        self.assertEquals(feature["feature_name"], self.TOKEN)

    def get_test_artifact(self):
        return Artifact("id", self.TOKEN, fake_method)

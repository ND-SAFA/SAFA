from django.test import TestCase
from data.artifact import Artifact
import mock

from mock import patch

EXPECTED_FEATURE = {"feature": "test"}


class TestArtifact(TestCase):

    @mock.patch("TestArtifact.fake_method", mock.MagicMock(return_value=EXPECTED_FEATURE))
    def test_get_feature(self):
        artifact = self.get_test_artifact()
        feature = artifact.get_feature()
        self.assertEquals(feature, EXPECTED_FEATURE)

    def get_test_artifact(self):
        return Artifact("id", "token", self.fake_method)

    @staticmethod
    def fake_method(x):
        pass

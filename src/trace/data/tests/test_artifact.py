from copy import copy

from django.test import TestCase

from trace.data.artifact import Artifact
from mock import patch

TEST_FEATURE = {"feature_name": "feature_value"}


def fake_method(text):
    return copy(TEST_FEATURE)


class TestArtifact(TestCase):

    def test_get_feature(self):
        expected_feature = copy(TEST_FEATURE)

        test_artifact = self.get_test_artifact()
        feature = test_artifact.get_feature()
        self.assertEquals(feature, expected_feature)

        # second time calling get_feature should not call feature_func again
        TEST_FEATURE["feature_name"] = "changed"
        feature = test_artifact.get_feature()
        self.assertEquals(feature, expected_feature)

    def get_test_artifact(self):
        return Artifact("id", "token", fake_method)

from unittest import TestCase

from data.github.gartifacts.gartifact_type import GArtifactType
from data.github.gtraces.glink import GLink
from data.github.gtraces.glink_processor import GLinkProcessor
from data.github.gtraces.glink_store import GLinkStore


class TestGLinkProcessor(TestCase):
    """
    Tests processing functions on glink store.
    """

    def test_get_linked_artifacts(self):
        """
        Verifies the correctness of calculating linked artifacts.
        """
        glink_store = GLinkStore()
        glink_store.add_link(GArtifactType.COMMIT, GArtifactType.ISSUE, GLink("1", "1"))
        glink_processor = GLinkProcessor(glink_store)
        issues, pulls, commits = glink_processor.get_linked_artifact_ids()
        self.assertListEqual(["1"], issues)
        self.assertEqual(0, len(pulls))
        self.assertListEqual(["1"], commits)

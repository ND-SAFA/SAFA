from unittest import TestCase

from tgen.data.github.gartifacts.gartifact_set import GArtifactSet
from tgen.data.github.gartifacts.gartifact_type import GArtifactType
from tgen.data.github.gtraces.glink import GLink
from tgen.data.github.gtraces.glink_processor import GLinkProcessor
from tgen.data.github.gtraces.glink_store import GLinkStore


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

    def test_get_transitive_traces(self):
        """
        Verifies that transitive traces are able to be detected and created.
        :return:
        """
        upper = GArtifactSet([GLink("S1", "T1"), GLink("S2", "T2")], GArtifactType.LINK)
        lower = GArtifactSet([GLink("T1", "C1"), GLink("T3", "C2")], GArtifactType.LINK)
        transitive_traces = GLinkProcessor.get_transitive_traces(upper, lower)
        self.assertEqual(1, len(transitive_traces))
        t = transitive_traces[0]
        self.assertEqual("S1", t.source)
        self.assertEqual("C1", t.target)

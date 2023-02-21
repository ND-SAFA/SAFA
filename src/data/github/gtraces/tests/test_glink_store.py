import os
from unittest import TestCase

from data.github.gartifacts.gartifact_set import GArtifactSet
from data.github.gartifacts.gartifact_type import GArtifactType
from data.github.github_constants import COMMIT_ARTIFACT_FILE, ISSUE_ARTIFACT_FILE, PULL_ARTIFACT_FILE
from data.github.gtraces.glink_store import GTraceStore
from testres.paths.paths import GITHUB_REPO_ARTIFACTS_DIR

COMMIT_ID = "85fdb4e8f2b90adf1b9604b93cab78fa21ff237f"
PULL_ID = "3"
ISSUE_ID = "1"
ISSUE_ID_2 = "2"


class TestGLinkStore(TestCase):
    issues = GArtifactSet.load(os.path.join(GITHUB_REPO_ARTIFACTS_DIR, ISSUE_ARTIFACT_FILE))
    pulls = GArtifactSet.load(os.path.join(GITHUB_REPO_ARTIFACTS_DIR, PULL_ARTIFACT_FILE))
    commits = GArtifactSet.load(os.path.join(GITHUB_REPO_ARTIFACTS_DIR, COMMIT_ARTIFACT_FILE))

    def test_linked_artifacts(self):
        store = self.load_store()
        issues, pulls, commits = store.get_linked_artifact_ids()
        self.assertSetEqual({ISSUE_ID, ISSUE_ID_2}, set(issues))
        self.assertSetEqual({PULL_ID}, set(pulls))
        self.assertSetEqual({COMMIT_ID}, set(commits))

    def test_parse_links(self):
        store = self.load_store()
        expected_links = [((GArtifactType.COMMIT, COMMIT_ID), (GArtifactType.ISSUE, ISSUE_ID)),
                          ((GArtifactType.COMMIT, COMMIT_ID), (GArtifactType.PULL, PULL_ID)),
                          ((GArtifactType.PULL, PULL_ID), (GArtifactType.ISSUE, ISSUE_ID)),
                          ((GArtifactType.ISSUE, ISSUE_ID), (GArtifactType.ISSUE, ISSUE_ID_2))
                          ]
        self.assert_equals(store, expected_links)

    def load_store(self) -> GTraceStore:
        store = GTraceStore()
        store.parse_links(self.issues, self.pulls, self.commits)
        return store

    def assert_equals(self, store, identifiers):
        self.assertEqual(len(identifiers), len(store), msg=str(store))
        for source_identifier, target_identifier in identifiers:
            self.assert_contains(store, source_identifier, target_identifier)

    def assert_contains(self, store, source_identifier, target_identifier):
        source_type, source_id = source_identifier
        target_type, target_id = target_identifier
        assert source_type in store.trace_store, f"{source_type} is not one of {store.keys()}."
        assert target_type in store.trace_store[source_type], f"Store does not contain target type: {target_type}"
        links = store.trace_store[source_type][target_type]
        links_display = []
        for link in links:
            if link.source == source_id and link.target == target_id:
                return
            links_display.append(f"{link.source}-{link.target}")
        links_display = ",".join(links_display)
        self.fail(f"Searched {source_type}->{target_type}. Could not find {source_id}-{target_id} in {links_display}")

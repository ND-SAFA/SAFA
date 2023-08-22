from typing import List, Tuple
from unittest import TestCase

from tgen.common.constants.deliminator_constants import COMMA
from tgen.data.github.gtraces.glink_finder import GLinkTarget
from tgen.data.github.gtraces.glink_store import GLinkStore
from tgen.testres.testprojects.github_test_project import GithubTestProject


class TestGTraceStore(TestCase):
    """
    Tests ability to store trace links and calculated linked artifacts.
    """

    def test_parse_links(self):
        """
        Tests that loading test project contains expected links.
        """
        store = self.load_store()
        self.assert_equals(store, GithubTestProject.get_expected_links())

    def assert_equals(self, store: GLinkStore, identifiers: List[Tuple[GLinkTarget, GLinkTarget]]) -> None:
        """
        Verifies that links contains exactly the links specified.
        :param store: The store containing links.
        :param identifiers: Identifiers of links to contain.
        :return: None
        """
        self.assertEqual(len(identifiers), len(store), msg=str(store))
        for source_identifier, target_identifier in identifiers:
            self.assert_contains(store, source_identifier, target_identifier)

    def assert_contains(self, store, source_identifier, target_identifier) -> None:
        """
        Verifies that store contains links between given source and target artifacts.
        :param store: Store containing links.
        :param source_identifier: Source ID and type.
        :param target_identifier: Target ID and type.
        :return: None
        """
        source_id, source_type = source_identifier
        target_id, target_type = target_identifier
        assert source_type in store, f"{source_type} is not one of {store.get_source_types()}."
        assert target_type in store[source_type], f"Store does not contain target type: {target_type}"
        links = store[source_type][target_type]
        links_display = []
        for link in links:
            if link.source == source_id and link.target == target_id:
                return
            links_display.append(f"{link.source}-{link.target}")
        links_display = COMMA.join(links_display)
        self.fail(f"Searched {source_type}->{target_type}. Could not find {source_id}-{target_id} in {links_display}")

    @staticmethod
    def load_store() -> GLinkStore:
        """
        Create store with test project.
        :return: Store with traces in project.
        """
        issues = GithubTestProject.get_issues()
        pulls = GithubTestProject.get_pulls()
        commits = GithubTestProject.get_commits()
        store = GLinkStore()
        store.add_artifact_links(issues, pulls, commits)
        return store

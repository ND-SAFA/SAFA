import unittest
from typing import Tuple

from tgen.data.github.gartifacts.gartifact_type import GArtifactType
from tgen.data.github.gartifacts.gissue import GIssue
from tgen.data.github.gtraces.glink_finder import GLinkTarget, LinkFinder


class TestLinkFinder(unittest.TestCase):
    """
    Tests ability to extract links from repository.
    """

    def test_search_issue_links(self):
        kwargs = {
            "issue_id": "5",
            "title": "Fix PR #2",
            "body": "This issue to address https://github.com/ND-SAFA/fend/pull/2",
            "comments": ["This might be addressed in #1."],
            "create_time": None,
            "close_time": None
        }
        issue = GIssue(**kwargs)
        links = LinkFinder.search_issue_links(issue)
        self.assertEqual(2, len(links))
        self._assert_link_equal(("2", "pull"), links[0])
        self._assert_link_equal(("1", "issue"), links[1])

    def test_search_multi(self):
        """
        Tests ability to find different types of links in text.
        """
        text = "Fixed with PR: #9, #10, https://github.com/ND-SAFA/fend/pull/3, https://github.com/ND-SAFA/fend/issues/7"
        links = LinkFinder.search_links(text)
        self.assertEqual(4, len(links))
        self._assert_link_equal(("9", "pull"), links[0])
        self._assert_link_equal(("10", "issue"), links[1])
        self._assert_link_equal(("3", "pull"), links[2])
        self._assert_link_equal(("7", "issue"), links[3])

    def test_search_for_autolink(self):
        """
        Tests that autolinks in text are properly extracted.
        """
        text = "This pull request fixes #1 in conjuction with PR #9. #10 continues to be in progress"
        links = LinkFinder.search_links(text)

        self.assertEqual(3, len(links))
        self._assert_link_equal(("9", "pull"), links[0])
        self._assert_link_equal(("1", "issue"), links[1])
        self._assert_link_equal(("10", "issue"), links[2])

    def test_search_url(self):
        """
        Tests the ability to extract GitHub link through URL reference.
        """
        url_link = LinkFinder.search_links("https://github.com/ND-SAFA/fend/pull/9")
        self.assertEqual(1, len(url_link))
        self._assert_link_equal(("9", "pull"), url_link[0])

    def test_use_case(self):
        commit = "Merge pull request #1 from eclipse-iceoryx/master Merge from master # # Pre-Review Checklist for the PR Author 1 . [ ] Branch follows the naming format ( ` iox- # 123-this-is-a-branch ` ) 1 . [ ] Commits messages are according to this [ guideline ] [ commit-guidelines ] - [ ] Commit messages have the issue ID ( ` iox- # 123 commit text ` ) - [ ] Commit messages are signed ( ` git commit -s ` ) - [ ] Commit author matches [ Eclipse Contributor Agreement ] [ eca ] ( and ECA is signed ) 1 . [ ] Update the PR title - Follow the same conventions as for commit messages - Link to the relevant issue 1 . [ ] Relevant issues are linked 1 . [ ] Add sensible notes for the reviewer 1 . [ ] All checks have passed 1 . [ ] Assign PR to reviewer [ commit-guidelines ] : https : //tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html [ eca ] : http : //www.eclipse.org/legal/ECA.php # # Notes for Reviewer # # Checklist for the PR Reviewer - [ ] Commits are properly organized and messages are according to the guideline - [ ] Code according to our coding style and naming conventions - [ ] Unit tests have been written for new behavior - [ ] Public API changes are documented via doxygen - [ ] Copyright owner are updated in the changed files - [ ] PR title describes the changes # # Post-review Checklist for the PR Author 1 . [ ] All open points are addressed and tracked via issues # # Post-review Checklist for the Eclipse Committer 1 . [ ] All checkboxes in the PR checklist are checked or crossed out 1 . [ ] Merge # # References - Closes * * TBD * *"
        links = LinkFinder.search_links(commit)
        self.assertEqual(1, len(links))

    def _assert_link_equal(self, expected: Tuple[str, str], result: GLinkTarget):
        """
        Verifies content of GitHub Link.
        """
        a_id, a_type = result
        e_id, e_type = expected
        self.assertEqual(e_id, a_id)
        self.assertEqual(GArtifactType[e_type.upper()], a_type, msg=f"{a_id}:")

import unittest
from typing import Tuple

from data.github.entities.github_artifact_type import GithubArtifactType
from data.github.entities.github_issue import GithubIssue
from data.github.link_extracter import GithubLink, LinkExtractor


class TestLinkExtracter(unittest.TestCase):
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
        issue = GithubIssue(**kwargs)
        links = LinkExtractor.search_issue_links(issue)
        self.assertEqual(2, len(links))
        self._assert_link_equal(("2", "pull_request"), links[0])
        self._assert_link_equal(("1", "issue"), links[1])

    def test_search_multi(self):
        """
        Tests ability to find different types of links in text.
        """
        text = "Fixed with PR: #9, #10, https://github.com/ND-SAFA/fend/pull/3, https://github.com/ND-SAFA/fend/issues/7"
        links = LinkExtractor.search_links(text)
        self.assertEqual(4, len(links))
        self._assert_link_equal(("9", "pull_request"), links[0])
        self._assert_link_equal(("10", "issue"), links[1])
        self._assert_link_equal(("3", "pull_request"), links[2])
        self._assert_link_equal(("7", "issue"), links[3])

    def test_search_for_autolink(self):
        """
        Tests that autolinks in text are properly extracted.
        """
        text = "Fixed with PR: #9 and working on #10"
        links = LinkExtractor.search_links(text)

        self.assertEqual(2, len(links))
        self._assert_link_equal(("9", "pull_request"), links[0])
        self._assert_link_equal(("10", "issue"), links[1])

    def test_search_url(self):
        """
        Tests the ability to extract GitHub link through URL reference.
        """
        url_link = LinkExtractor.search_links("https://github.com/ND-SAFA/fend/pull/9")
        self.assertEqual(1, len(url_link))
        self._assert_link_equal(("9", "pull_request"), url_link[0])

    def _assert_link_equal(self, expected: Tuple[str, str], result: GithubLink):
        """
        Verifies content of GitHub Link.
        """
        a_id, a_type = result
        e_id, e_type = expected
        self.assertEqual(e_id, a_id)
        self.assertEqual(GithubArtifactType[e_type.upper()], a_type, msg=f"{a_id}:")

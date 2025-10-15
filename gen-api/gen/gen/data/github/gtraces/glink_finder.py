import re
from typing import List, Tuple, Union

from gen.data.github.gartifacts.gartifact_type import GArtifactType
from gen.data.github.gartifacts.gissue import GIssue

AutoLinkPatterns = [  # patterns are uncased
    ["\\bpr[,|.|\s|:]{0,1}\s+#\d+\\b", GArtifactType.PULL, "#"],  # Matches [PR: #2]
    ["\\bpull[,|.|\s|:]{0,1}\s+#\d+\\b", GArtifactType.PULL, "#"],  # Matches  [Pull Request #2]
    ["\\bpull request[,|.|\s|:]{0,1}\s+#\d+\\b", GArtifactType.PULL, "#"],
    # Matches pull request, s white space, and the autolink. [Pull Request #2]
    ["#\d+", GArtifactType.ISSUE, "#"],  # Matches: [Solves #3]
    ["pull\/\d+", GArtifactType.PULL, "/"],  # Matches: [https://github.com/org/repo/pull/2]
    ["issues\/\d+", GArtifactType.ISSUE, "/"]]  # Matches: [https://github.com/org/repo/issues/2]

GLinkTarget = Tuple[str, GArtifactType]


class LinkFinder:
    """
    Responsible for finding links to Github artifacts in bodies of text.
    """

    @staticmethod
    def search_issue_links(issue: GIssue) -> List[GLinkTarget]:
        """
        Searches through issue body and comments for linked artifacts.
        :param issue: The issue to search for links to.
        :return: List of links containing given issue.
        """
        issue_text_bodies = [issue.title, issue.body] + issue.comments
        issue_text_bodies = [b for b in issue_text_bodies if b is not None]
        issue_links = LinkFinder.search_links(issue_text_bodies)
        return issue_links

    @staticmethod
    def search_links(texts: Union[List[str], str]) -> List[GLinkTarget]:
        """
        Searches for autolinks or references to repository issues.
        :param texts: The text to search for links within.
        :return: List of links to GitHub artifacts.
        """
        if texts is None:
            return []
        if isinstance(texts, str):
            return LinkFinder.search_links([texts])
        links = {}
        for text in texts:
            for pattern, github_type, delimiter in AutoLinkPatterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                for link_matches in matches:
                    issue_id = link_matches.split(delimiter)[1].strip()
                    if issue_id not in links:
                        links[issue_id] = github_type
        github_links = [github_link for github_link in links.items()]
        return github_links

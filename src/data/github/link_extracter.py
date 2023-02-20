import re
from typing import List, Tuple, Union

from data.github.entities.commit import Commit
from data.github.entities.github_artifact_type import GithubArtifactType
from data.github.entities.github_issue import GithubIssue
from data.github.entities.github_link import Link
from data.github.entities.github_pull import GithubPull
from data.github.entities.repository_artifact_set import RepositoryArtifactSet

GithubLink = Tuple[str, GithubArtifactType]
AutoLinkPatterns = [  # patterns are uncased
    ["\\bpr.+?#\d+\\b", GithubArtifactType.PULL_REQUEST, "#"],  # Matches: [PR: #2]
    ["\\bpull request.+?#\d+\\b", GithubArtifactType.PULL_REQUEST, "#"],  # Matches: [Pull Request #2]
    ["#\d+", GithubArtifactType.ISSUE, "#"],  # Matches: [Solves #3]
    ["pull\/\d+", GithubArtifactType.PULL_REQUEST, "/"],  # Matches: [https://github.com/org/repo/pull/2]
    ["issues\/\d+", GithubArtifactType.ISSUE, "/"]]  # Matches: [https://github.com/org/repo/issues/2]


class LinkExtractor:
    def __init__(self, repository_name: str):
        self.repository_name = repository_name

    def parse_links(self,
                    issues: RepositoryArtifactSet[GithubIssue],
                    pulls: RepositoryArtifactSet[GithubIssue],
                    commits: RepositoryArtifactSet[Commit]) -> Tuple[
        RepositoryArtifactSet[Link], RepositoryArtifactSet[Link], RepositoryArtifactSet[Link]]:
        issue2issue = []
        pull2issue = []
        pr2pr = []
        commit2pr = []
        commit2issue = []
        for issue in issues.artifacts:
            for target_id, target_type in self.search_issue_links(issue):
                if target_type == GithubArtifactType.ISSUE:
                    issue2issue.append(Link(issue.issue_id, target_id))
                elif target_type == GithubArtifactType.PULL_REQUEST:
                    pull2issue.append(Link(target_id, issue.issue_id))

        for pull in pulls.artifacts:
            for target_id, target_type in self.search_issue_links(pull):
                if target_type == GithubArtifactType.ISSUE:
                    pull2issue.append(Link(pull.issue_id, target_id))
                elif target_type == GithubArtifactType.PULL_REQUEST:
                    pr2pr.append(Link(pull.issue_id, target_id))

        for commit in commits.artifacts:
            commit_links = self.search_links(commit.content)
            for c_link in commit_links:
                artifact_id, artifact_type = c_link
                if artifact_type == GithubArtifactType.PULL_REQUEST:
                    commit2pr.append(Link(commit.commit_id, artifact_id))
                if artifact_type == GithubArtifactType.ISSUE:
                    commit2issue.append(Link(commit.commit_id, artifact_id))

        return RepositoryArtifactSet(pull2issue, GithubArtifactType.LINK), RepositoryArtifactSet(commit2pr,
                                                                                                 GithubArtifactType.LINK), RepositoryArtifactSet(
            commit2issue, GithubArtifactType.LINK)

    @staticmethod
    def search_issue_links(issue: Union[GithubIssue, GithubPull]) -> List[GithubLink]:
        """
        Searches through issue body and comments for linked artifacts.
        :param issue: The issue to search for links to.
        :return: List of links containing given issue.
        """
        issue_text_bodies = [issue.title, issue.body] + issue.comments
        issue_links = LinkExtractor.search_links(issue_text_bodies)
        return issue_links

    @staticmethod
    def search_links(texts: Union[List[str], str]) -> List[Tuple[str, GithubArtifactType]]:
        """
        Searches for autolinks or references to repository issues.
        :param texts: The text to search for links within.
        :return: List of links to GitHub artifacts.
        """
        if texts is None:
            return []
        if isinstance(texts, str):
            return LinkExtractor.search_links([texts])
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

from datetime import datetime
from typing import Dict, List

from github import PullRequest

from common_resources.tools.util.date_time_util import DateTimeUtil
from tgen.data.github.gartifacts.gissue import GIssue


class GPull(GIssue):
    """
    GithubArtifact representing pull request in repository.
    """

    def __init__(self,
                 issue_id: str,
                 title: str,
                 body: str,
                 comments: List[str],
                 create_time: datetime,
                 close_time: datetime,
                 commits: List[str]):
        """
        Initializes issue with given content.
        :param issue_id: The issue id.
        :param title: The title of the issue.
        :param body: The body of the issue.
        :param comments: The comments on the issue.
        :param create_time: The time the issue was created.
        :param close_time: The time the issue was closed.
        :param commits: The commits associated with pull request.
        """
        super().__init__(issue_id, title, body, comments, create_time, close_time)
        self.commits = commits

    @staticmethod
    def parse(pr: PullRequest) -> "PullRequest":
        """
        Creates GPull from Github pull request.
        :param pr: The github pull request object.
        :return: The created pull request.
        """
        comments = [comment.body for comment in pr.get_comments()]
        commits = [commit.sha for commit in pr.get_commits()]
        return GPull(pr.number,
                     pr.title,
                     pr.body,
                     comments,
                     pr.created_at,
                     pr.closed_at,
                     commits)

    @staticmethod
    def from_state_dict(state_dict: Dict) -> "PullRequest":
        """
        Constructs pull request from state dictionary.
        :param state_dict: Dictionary containing saved state of pull request.
        :return: Constructed GPull.
        """
        return GPull(state_dict["id"],
                     state_dict["title"],
                     state_dict["body"],
                     state_dict["comments"],
                     DateTimeUtil.read_datetime(state_dict["closed_at"]),
                     DateTimeUtil.read_datetime(state_dict["created_at"]),
                     state_dict["commits"])

    def get_state_dict(self):
        """
        :return: Returns the state dictionary of pull request.
        """
        return {
            "id": self.issue_id,
            "title": self.title,
            "body": self.body,
            "comments": self.comments,
            "closed_at": str(self.create_time),
            "created_at": str(self.close_time),
            "commits": self.commits
        }

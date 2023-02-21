import re
from datetime import datetime
from typing import Dict, List, Union

from github import Issue
from nltk import word_tokenize

from data.github.abstract_github_entity import AbstractGithubArtifact
from data.github.gartifacts.gartifact_type import GArtifactType
from util.date_time_util import DateTimeUtil
from util.override import overrides


class GIssue(AbstractGithubArtifact):
    """
    GithubArtifact representing issue in repository.
    """
    VALID_ARTIFACT_TYPES = [GArtifactType.PULL, GArtifactType.ISSUE]

    def __init__(self,
                 issue_id: str,
                 title: str,
                 body: str,
                 comments: List[str],
                 create_time: datetime,
                 close_time: datetime):
        """
        Initializes issue from content.
        :param issue_id: The id of the issue.
        :param title: The issue title
        :param body: The body of the issue.
        :param comments: The comments on the issue.
        :param create_time: The time the issue was created.
        :param close_time: The tiem the issue was closed.
        """
        self.issue_id = str(issue_id)
        self.title = title
        self.body = body
        self.comments = comments
        self.create_time = create_time
        self.close_time = close_time

    @overrides(AbstractGithubArtifact)
    def export(self, **kwargs) -> Union[Dict, None]:
        """
        Returns dictionary entry for exporting issue.
        :param kwargs: Additional parameters for modifying export process.
        :return: Dictionary entry.
        """
        if self.body is None:
            self.body = ""
        self.body = re.sub("<!-.*->", "", self.body)
        self.body = re.sub("```.*```", "", self.body, flags=re.DOTALL)
        self.body = " ".join(word_tokenize(self.body))
        return {"id": self.issue_id, "content": " ".join([self.title, self.body])}

    @overrides(AbstractGithubArtifact)
    def get_id(self) -> str:
        """
        :return: Returns the issue id.
        """
        return self.issue_id

    @overrides(AbstractGithubArtifact)
    def to_dict(self) -> Dict:
        """
        Returns the state dictionary of GIssue.
        :return: Dictionary containing current state of GIssue.
        """
        return {
            "id": self.issue_id,
            "title": self.title,
            "body": self.body,
            "comments": self.comments,
            "closed_at": None if self.create_time is None else str(self.create_time),
            "created_at": None if self.close_time is None else str(self.close_time)
        }

    @staticmethod
    @overrides(AbstractGithubArtifact)
    def read(row: Dict) -> "Issue":
        """
        Reads state dictionary and constructs issue from it.
        :param row: The state dictionary of GIssue.
        :return: Constructed GIssue.
        """
        return GIssue(row["id"],
                      row["title"],
                      row["body"],
                      row["comments"],
                      DateTimeUtil.read_datetime(row["closed_at"]),
                      DateTimeUtil.read_datetime(row["created_at"]))

    @staticmethod
    def parse(issue: Issue) -> "Issue":
        """
        Creates issue from official GitHub issue.
        :param issue: The issue to convert to local format.
        :return: Constructed GIssue.
        """
        comments = [comment.body for comment in issue.get_comments()]
        return GIssue(issue.number,
                      issue.title,
                      issue.body,
                      comments,
                      issue.created_at,
                      issue.closed_at)

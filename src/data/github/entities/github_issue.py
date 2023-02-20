import re
from datetime import datetime
from typing import Dict, List, Union

from github import Issue
from nltk import word_tokenize

from data.github.entities.abstract_github_artifact import AbstractGithubArtifact
from data.github.entities.github_artifact_type import GithubArtifactType
from data.github.github_utils import GithubUtils


class GithubIssue(AbstractGithubArtifact):
    VALID_ARTIFACT_TYPES = [GithubArtifactType.PULL_REQUEST, GithubArtifactType.ISSUE]

    def __init__(self,
                 issue_id: str,
                 title: str,
                 body: str,
                 comments: List[str],
                 create_time: datetime,
                 close_time: datetime):
        self.issue_id = str(issue_id)
        self.title = title
        self.body = body
        self.comments = comments
        self.create_time = create_time
        self.close_time = close_time

    def export(self, **kwargs) -> Union[Dict, None]:
        if self.body is None:
            self.body = ""
        self.body = re.sub("<!-.*->", "", self.body)
        self.body = re.sub("```.*```", "", self.body, flags=re.DOTALL)
        self.body = " ".join(word_tokenize(self.body))
        return {"id": self.issue_id, "content": " ".join([self.title, self.body])}

    def get_id(self) -> str:
        return self.issue_id

    @staticmethod
    def parse(issue: Issue) -> "Issue":
        comments = [comment.body for comment in issue.get_comments()]
        return GithubIssue(issue.number,
                           issue.title,
                           issue.body,
                           comments,
                           issue.created_at,
                           issue.closed_at)

    @staticmethod
    def read(row: Dict) -> "Issue":
        return GithubIssue(row["id"],
                           row["title"],
                           row["body"],
                           row["comments"],
                           GithubUtils.read_datetime(row["closed_at"]),
                           GithubUtils.read_datetime(row["created_at"]))

    def to_dict(self):
        return {
            "id": self.issue_id,
            "title": self.title,
            "body": self.body,
            "comments": self.comments,
            "closed_at": None if self.create_time is None else str(self.create_time),
            "created_at": None if self.close_time is None else str(self.close_time)
        }

from datetime import datetime
from typing import Dict, List

from github import PullRequest
from github.Issue import Issue

from data.github.github_utils import GithubUtils


class GithubPull(Issue):
    def __init__(self,
                 issue_id: str,
                 title: str,
                 body: str,
                 comments: List[str],
                 create_time: datetime,
                 close_time: datetime,
                 commits: List[str]):
        super().__init__(issue_id, title, body, comments, create_time, close_time)
        self.commits = commits

    @staticmethod
    def parse(pr: PullRequest) -> "PullRequest":
        comments = [comment.body for comment in pr.get_comments()]
        commits = [commit.sha for commit in pr.get_commits()]
        return GithubPull(pr.number,
                          pr.title,
                          pr.body,
                          comments,
                          pr.created_at,
                          pr.closed_at,
                          commits)

    @staticmethod
    def read(row: Dict) -> "PullRequest":
        return GithubPull(row["id"],
                          row["title"],
                          row["body"],
                          row["comments"],
                          GithubUtils.read_datetime(row["closed_at"]),
                          GithubUtils.read_datetime(row["created_at"]),
                          row["commits"])

    def to_dict(self):
        return {
            "id": self.issue_id,
            "title": self.title,
            "body": self.body,
            "comments": self.comments,
            "closed_at": str(self.create_time),
            "created_at": str(self.close_time),
            "commits": self.commits
        }

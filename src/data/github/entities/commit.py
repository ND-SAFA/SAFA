from typing import Dict, List, Union

from git import Commit

from data.github.entities.abstract_github_artifact import AbstractGithubArtifact

EMPTY_TREE_SHA = "4b825dc642cb6eb9a060e54bf8d69288fbee4904"


class Commit(AbstractGithubArtifact):

    def __init__(self, commit_id: str, content: str, diffs: List[str], files: List[str],
                 commit_time: str):
        """
        Construct commit containing id, summary, diff, affected files, commit time, and export variables (e.g. use code diff).
        :param commit_id: The commit SHA.
        :param content: The commit body to use as artifact body.
        :param diffs: The diff of the commit.
        :param files: List of file paths modified by this commit.
        :param commit_time: The time of commit.
        """
        self.commit_id = commit_id
        self.content = content
        self.diffs = diffs
        self.files = files
        self.commit_time = commit_time

    def get_id(self) -> str:
        """
        :return: Returns the SHA of the commit.
        """
        return self.commit_id

    def export(self, dataset_type: str = "NL") -> Union[Dict, None]:
        """
        Exports commit for saving.
        :return:
        """
        body = self.content
        if dataset_type == "PL":
            body += " " + "\n".join(self.diffs)
        return {"id": self.commit_id, "content": body}

    def to_dict(self):
        return {
            "commit_id": self.commit_id,
            "summary": self.content,
            "diff": list(self.diffs),
            "files": self.files,
            "commit_time": str(self.commit_time)
        }

    @staticmethod
    def parse_commit(commit: Commit) -> "Commit":
        id = commit.hexsha
        content = commit.message
        create_time = commit.committed_datetime
        commit_diff = Commit.get_commit_diff(commit)
        files = list(commit.stats.files)
        return Commit(commit_id=id,
                      content=content,
                      diffs=list(commit_diff),
                      files=files,
                      commit_time=create_time)

    @staticmethod
    def get_commit_diff(commit: Commit) -> List[str]:
        """
        Returns list of changed lines in commit. Additions are pre-pended with + and deletions with -.
        :param commit: The commit whose diff is returned.
        :return: List of changed lined.
        """
        has_parent = len(commit.parents) > 0
        parent = commit.parents[0] if has_parent else commit
        commit = commit if has_parent else EMPTY_TREE_SHA
        differs = set()
        for diff in parent.diff(commit, create_patch=True):
            diff_lines = str(diff).split("\n")
            for diff_line in diff_lines:
                if diff_line.startswith("+") or diff_line.startswith("-") and '@' not in diff_line and not diff_line.startswith("---"):
                    differs.add(diff_line)
        return list(differs)

    @staticmethod
    def read(row: Dict) -> "Commit":
        return Commit(commit_id=row["commit_id"],
                      content=row["summary"],
                      diffs=row["diff"],
                      files=row["files"],
                      commit_time=row['commit_time'])

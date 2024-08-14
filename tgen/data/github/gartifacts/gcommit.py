from typing import Callable, Dict, List, Union

from common_resources.tools.constants.symbol_constants import NEW_LINE
from git import Commit

from common_resources.tools.util.override import overrides
from tgen.data.github.abstract_github_entity import AbstractGithubArtifact

EMPTY_TREE_SHA = "4b825dc642cb6eb9a060e54bf8d69288fbee4904"


class GCommit(AbstractGithubArtifact):
    """
    Represents a commit in a repository.
    """

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

    @overrides(AbstractGithubArtifact)
    def get_id(self) -> str:
        """
        :return: Returns the SHA of the commit.
        """
        return self.commit_id

    @overrides(AbstractGithubArtifact)
    def as_dataframe_entry(self, dataset_type: str = "NL") -> Union[Dict, None]:
        """
        Exports commit for saving.
        :param dataset_type: The type of dataset, either NL or PL.
        :return:
        """
        body = NEW_LINE.join(self.diffs) if dataset_type == "PL" else self.content
        return {"id": self.commit_id, "content": body}

    @overrides(AbstractGithubArtifact)
    def get_state_dict(self) -> Dict:
        """
        :return: Returns the state dictionary associated with commit.
        """
        return {
            "commit_id": self.commit_id,
            "summary": self.content,
            "diff": list(self.diffs),
            "files": self.files,
            "commit_time": str(self.commit_time)
        }

    @staticmethod
    def parse_commit(commit: Commit) -> "GCommit":
        """
        Parses GCommit from git commit.
        :param commit: The commit from local repository.
        :return: Constructed GCommit.
        """
        id = commit.hexsha
        content = commit.message
        create_time = commit.committed_datetime
        commit_diff = GCommit.get_commit_diff(commit)
        files = list(commit.stats.files)
        return GCommit(commit_id=id,
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
        for diff in parent.diff(commit, create_patch=True):  # TODO: Use actual diff objects instead of parsing string
            diff_lines = str(diff).split(NEW_LINE)
            for diff_line in diff_lines:
                if diff_line.startswith("+") or diff_line.startswith("-") and '@' not in diff_line and not diff_line.startswith("---"):
                    differs.add(diff_line)
        return list(differs)

    @staticmethod
    @overrides(AbstractGithubArtifact)
    def from_state_dict(state_dict: Dict) -> "GCommit":
        """
        Create commit from state stored on disk.
        :param state_dict: Row in data frame.
        :return: Constructed GCommit.
        """
        return GCommit(commit_id=state_dict["commit_id"],
                       content=state_dict["summary"],
                       diffs=state_dict["diff"],
                       files=state_dict["files"],
                       commit_time=state_dict['commit_time'])

    def clean_content(self, cleaner: Callable[[str], str]) -> None:
        """
        Cleans content of commit.
        :param cleaner: The cleaning function return cleaned string.
        :return: None
        """
        self.content = cleaner(self.content)

import os
import re

from data.github.gartifacts.gartifact_set import GArtifactSet
from data.github.gartifacts.gartifact_type import GArtifactType
from data.github.gartifacts.gcommit import GCommit
from data.github.github_constants import COMMIT_ARTIFACT_FILE, \
    COMMIT_DIFF_ARTIFACT_FILE, GENERIC_COMMIT_HEADERS, ISSUE_ARTIFACT_FILE, \
    MIN_WORD_LENGTH, PULL_ARTIFACT_FILE
from data.github.gtraces.glink_store import GTraceStore
from data.github.repository_downloader import logger


class GithubRepositoryExtracter:
    """
    Reads parsed artifacts and cleans them for export.
    """
    SOURCE_FILE = "sources.csv"
    TARGET_FILE = "targets.csv"
    LINK_FILE = "links.csv"

    def __init__(self, repo_path: str):
        """
        Initializes extracter for given repo and
        :param repo_path: Path to the local repository.
        """
        self.repo_path = repo_path
        self.issues = self.__read_artifact_set(ISSUE_ARTIFACT_FILE)
        self.pulls = self.__read_artifact_set(PULL_ARTIFACT_FILE)
        self.commits = self.__read_artifact_set(COMMIT_ARTIFACT_FILE)
        self.trace_store = GTraceStore()

    def extract(self, output_path: str):
        self.pre_process()
        self.save(output_path=output_path)

    def pre_process(self):
        # A. Remove merge commits
        self.commits = self.__remove_default_commits(self.commits)
        self.commits = self.__remove_short_commits(self.commits, MIN_WORD_LENGTH)
        self.commits = self.__clean_commits(self.commits)

        # B. Parse entities
        self.trace_store.parse_links(self.issues, self.pulls, self.commits)
        linked_issues, linked_pulls, linked_commits = self.trace_store.get_linked_artifact_ids()
        self.issues = self.issues.filter(linked_issues)
        self.pulls = self.pulls.filter(linked_pulls)
        self.commits = self.commits.filter(linked_commits)

    def save(self, output_path: str):
        # A. Paths
        issue_output_path = os.path.join(output_path, ISSUE_ARTIFACT_FILE.replace(".json", ".csv"))
        pull_output_path = os.path.join(output_path, PULL_ARTIFACT_FILE.replace(".json", ".csv"))
        commit_output_path = os.path.join(output_path, COMMIT_ARTIFACT_FILE.replace(".json", ".csv"))
        commit_diff_output_path = os.path.join(output_path, COMMIT_DIFF_ARTIFACT_FILE.replace(".json", ".csv"))

        # B. Export
        logger.info("Saving Artifacts")
        artifacts = [self.issues, self.pulls, self.commits]
        paths = [issue_output_path, pull_output_path, commit_output_path]
        for artifact_set, path in zip(artifacts, paths):
            artifact_set.save(path, columns=["id", "content"], dataset_type="NL")
            logger.info(f"{os.path.basename(path)}: {len(artifact_set)}")
        self.commits.save(commit_diff_output_path, columns=["id", "content"], dataset_type="PL")
        self.trace_store.save(output_path)

    def __read_artifact_set(self, artifact_file_name: str) -> GArtifactSet:
        commit_file_path = os.path.join(self.repo_path, artifact_file_name)
        return GArtifactSet.load(commit_file_path)

    @staticmethod
    def __remove_default_commits(commit_artifact_set: GArtifactSet[GCommit]) -> GArtifactSet[GCommit]:
        """
        Removes GitHub generated commits including pull requests merge and reverts.
        :param commit_artifact_set: The artifact set containing commits.
        :return: User created-commits.
        """
        commits = []
        for commit in commit_artifact_set.artifacts:
            hits = [re.search(generic_header, commit.content) for generic_header in GENERIC_COMMIT_HEADERS]
            hits = [h for h in hits if h is not None]
            if len(hits) == 0:
                commits.append(commit)
        return GArtifactSet(commits, GArtifactType.COMMIT)

    @staticmethod
    def __remove_short_commits(commit_artifact_set: GArtifactSet[GCommit], min_artifact_length: int) -> GArtifactSet[GCommit]:
        """
        Removes commits whose body is less than minimum artifact length defined in constants.
        :param commit_artifact_set: The set of commits in repository.
        :param min_artifact_length: The minimum length of the artifacts to keep.
        :return: Commits with equal or greater content length than minimum.
        """
        long_messages = [a for a in commit_artifact_set.artifacts if len(a.content.split(" ")) >= min_artifact_length]
        return GArtifactSet(long_messages, GArtifactType.COMMIT)

    @staticmethod
    def __clean_commits(commit_artifact_set: GArtifactSet[GCommit]) -> GArtifactSet[GCommit]:
        """
        Removes redundant text and strips content.
        :param commit_artifact_set: The set of artifacts to clean.
        :return: The cleaned artifacts.
        """
        SIGNED_OFF_REGEX = "Signed-off-by.+$"
        for a in commit_artifact_set.artifacts:
            a.clean(lambda s: re.sub(SIGNED_OFF_REGEX, "", s).strip())
        return commit_artifact_set

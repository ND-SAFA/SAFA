import os
import re
from typing import List

from data.github.entities.commit import Commit
from data.github.entities.github_artifact_type import GithubArtifactType
from data.github.entities.github_link import Link
from data.github.entities.repository_artifact_set import RepositoryArtifactSet
from data.github.github_constants import ARTIFACT_PATH, COMMIT2ISSUE_ARTIFACT_FILE, COMMIT_ARTIFACT_FILE, \
    GENERIC_COMMIT_HEADERS, ISSUE_ARTIFACT_FILE, \
    MIN_ARTIFACT_LENGTH, PULL2ISSUE_ARTIFACT_FILE, PULL_ARTIFACT_FILE
from data.github.link_extracter import LinkExtractor


class GithubRepositoryExtracter:
    """
    Reads parsed artifacts and cleans them for export.
    """
    SOURCE_FILE = "sources.csv"
    TARGET_FILE = "targets.csv"
    LINK_FILE = "links.csv"

    def __init__(self, repo_name: str):
        """
        Initializes extracter for given repo and
        :param repo_name:
        :param dataset_type:
        :param output_path:
        """
        self.repo_name = repo_name
        self.repo_path = os.path.join(ARTIFACT_PATH, repo_name)
        self.issues = self.__read_artifact_set(ISSUE_ARTIFACT_FILE)
        self.pulls = self.__read_artifact_set(PULL_ARTIFACT_FILE)
        self.commits = self.__read_artifact_set(COMMIT_ARTIFACT_FILE)

    def extract(self, output_path: str):

        # A. Remove merge commits
        self.commits = self.__remove_default_commits(self.commits)
        self.commits = self.__remove_short_commits(self.commits, MIN_ARTIFACT_LENGTH)

        # B. Parse links
        print("Parsing links...")
        link_extractor = LinkExtractor(self.repo_name)
        pull2issue, commit2pr, commit2issue = link_extractor.parse_links(self.issues, self.pulls, self.commits)
        print("Done!")

        # C. remove artifacts do not have associated links
        print("pruning unused artifacts...")
        commits, pulls, issues, commit2issue, pull2issue = self.__remove_orphan_artifacts(
            commits=self.commits,
            pulls=self.pulls,
            issues=self.issues,
            commit2issue=commit2issue.artifacts,
            pull2issue=pull2issue.artifacts
        )

        # 1. Export source artifacts (issues)
        self.__save(output_path=output_path, issues=issues, pulls=pulls, commits=commits, commit2issue=commit2issue,
                    pull2issue=pull2issue)
        print("# links:", len(commit2issue) + len(pull2issue))

    def __save(self, output_path: str, issues, pulls, commits, commit2issue, pull2issue):
        # A. Paths
        issue_output_path = os.path.join(output_path, ISSUE_ARTIFACT_FILE.replace(".json", ".csv"))
        pull_output_path = os.path.join(output_path, PULL_ARTIFACT_FILE.replace(".json", ".csv"))
        commit_output_path = os.path.join(output_path, COMMIT_ARTIFACT_FILE.replace(".json", ".csv"))
        commit2issue_output_path = os.path.join(output_path, COMMIT2ISSUE_ARTIFACT_FILE.replace(".json", ".csv"))
        pull2issue_output_path = os.path.join(output_path, PULL2ISSUE_ARTIFACT_FILE.replace(".json", ".csv"))

        # B. Export
        print("Saving Artifacts")
        issues.export_training_data(issue_output_path, columns=["id", "content"])
        pulls.export_training_data(pull_output_path, columns=["id", "content"])
        for dataset_type in ["pl", "nl"]:
            commits.export_training_data(commit_output_path, columns=["id", "content"], dataset_type=dataset_type)
        commit2issue.export_training_data(commit2issue_output_path, columns=["source", "target"])
        pull2issue.export_training_data(pull2issue_output_path, columns=["source", "target"])

    @staticmethod
    def __remove_default_commits(commit_artifact_set: RepositoryArtifactSet[Commit]) -> RepositoryArtifactSet[Commit]:
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
        return RepositoryArtifactSet(commits, GithubArtifactType.COMMIT)

    @staticmethod
    def __remove_short_commits(commit_artifact_set: RepositoryArtifactSet[Commit], min_artifact_length: int) -> RepositoryArtifactSet[
        Commit]:
        """
        Removes commits whose body is less than minimum artifact length defined in constants.
        :param commit_artifact_set: The set of commits in repository.
        :param min_artifact_length: The minimum length of the artifacts to keep.
        :return: Commits with equal or greater content length than minimum.
        """
        long_messages = [a for a in commit_artifact_set.artifacts if len(a.content.split(" ")) >= min_artifact_length]
        return RepositoryArtifactSet(long_messages, GithubArtifactType.COMMIT)

    @staticmethod
    def __remove_orphan_artifacts(commits: RepositoryArtifactSet,
                                  pulls: RepositoryArtifactSet,
                                  issues: RepositoryArtifactSet,
                                  commit2issue: List[Link],
                                  pull2issue: List[Link]
                                  ):
        """
        Removes any artifacts not containing at least one link in trace links.
        :param commits: The commits of the repository.
        :param pulls: The pull requests of the repository.
        :param issues: The issues of the repository.
        :param commit2issue: The trace links between commit and issues.
        :param pull2issue: The trace links between pull requests and issues.
        :return: Processed entities including artifacts and trace links.
        """
        # 1. Throw out links with null pointers
        commit2issue = [t for t in commit2issue if t.source in commits and t.target in issues]
        pull2issue = [t for t in pull2issue if t.source in pulls and t.target in issues]

        # 2. Keep artifacts with at least one link
        linked_commits = set([link.source for link in commit2issue])
        linked_pulls = set([link.source for link in pull2issue])
        linked_issues = [link.target for link in commit2issue]
        linked_issues.extend([link.target for link in pull2issue])
        linked_issues = set(linked_issues)

        linked_commits = [commit_id for commit_id in commits.artifact_ids if commit_id in linked_commits]
        linked_pulls = [pull_id for pull_id in pulls.artifact_ids if pull_id in linked_pulls]
        linked_issues = [pull_id for pull_id in issues.artifact_ids if pull_id in linked_issues]

        filtered_commits = commits.filter(linked_commits)
        filtered_pulls = pulls.filter(linked_pulls)
        filtered_issues = issues.filter(linked_issues)

        return filtered_commits, filtered_pulls, filtered_issues, RepositoryArtifactSet(commit2issue,
                                                                                        GithubArtifactType.LINK), RepositoryArtifactSet(
            pull2issue, GithubArtifactType.LINK)

    def __read_artifact_set(self, artifact_file_name: str) -> RepositoryArtifactSet:
        commit_file_path = os.path.join(self.repo_path, artifact_file_name)
        return RepositoryArtifactSet.load(commit_file_path)

import os
from typing import List, Tuple

from tgen.data.github.gartifacts.gartifact_set import GArtifactSet
from tgen.data.github.gartifacts.gartifact_type import GArtifactType
from tgen.data.github.github_constants import COMMIT_ARTIFACT_FILE, ISSUE_ARTIFACT_FILE, PULL_ARTIFACT_FILE
from tgen.data.github.gtraces.glink_finder import GLinkTarget
from tgen.testres.paths.paths import TEST_DATA_DIR


class GithubTestProject:
    """
    Provides access to ground-truth of github project.
    """
    ISSUE_ID = "1"
    ISSUE_ID_2 = "2"
    PULL_ID = "3"
    COMMIT_ID = "85fdb4e8f2b90adf1b9604b93cab78fa21ff237f"
    PROJECT_PATH = os.path.join(TEST_DATA_DIR, "github", "artifacts")
    ARTIFACT_PATHS = {
        GArtifactType.ISSUE: os.path.join(PROJECT_PATH, ISSUE_ARTIFACT_FILE),
        GArtifactType.PULL: os.path.join(PROJECT_PATH, PULL_ARTIFACT_FILE),
        GArtifactType.COMMIT: os.path.join(PROJECT_PATH, COMMIT_ARTIFACT_FILE)
    }

    @staticmethod
    def get_issues() -> GArtifactSet:
        """
        :return: Returns artifact set of issues.
        """
        return GArtifactSet.load(GithubTestProject.get_path(GArtifactType.ISSUE))

    @staticmethod
    def get_pulls() -> GArtifactSet:
        """
        :return: Returns artifact set of issues.
        """
        return GArtifactSet.load(GithubTestProject.get_path(GArtifactType.PULL))

    @staticmethod
    def get_commits() -> GArtifactSet:
        """
        :return: Returns artifact set of issues.
        """
        return GArtifactSet.load(GithubTestProject.get_path(GArtifactType.COMMIT))

    @staticmethod
    def get_expected_links() -> List[Tuple[GLinkTarget, GLinkTarget]]:
        """
        :return: Returns the links established by the project.
        """
        return [
            ((GithubTestProject.COMMIT_ID, GArtifactType.COMMIT), (GithubTestProject.ISSUE_ID, GArtifactType.ISSUE)),
            ((GithubTestProject.COMMIT_ID, GArtifactType.COMMIT), (GithubTestProject.PULL_ID, GArtifactType.PULL)),
            ((GithubTestProject.PULL_ID, GArtifactType.PULL), (GithubTestProject.ISSUE_ID, GArtifactType.ISSUE)),
            ((GithubTestProject.ISSUE_ID, GArtifactType.ISSUE), (GithubTestProject.ISSUE_ID_2, GArtifactType.ISSUE))
        ]

    @staticmethod
    def get_issue_ids() -> List[str]:
        """
        :return: Returns the issue ids of the github project.
        """
        return [GithubTestProject.ISSUE_ID, GithubTestProject.ISSUE_ID_2]

    @staticmethod
    def get_pull_ids() -> List[str]:
        """
        :return: Returns the pull request ids.
        """
        return [GithubTestProject.PULL_ID]

    @staticmethod
    def get_commit_ids() -> List[str]:
        """
        :return: Returns the commit ids.
        """
        return [GithubTestProject.COMMIT_ID]

    @staticmethod
    def get_path(artifact_type: GArtifactType) -> str:
        """
        Returns the path to the artifact file for give type.
        :param artifact_type: The artifact type of the file to return.
        :return: The path to the artifact file.
        """
        return GithubTestProject.ARTIFACT_PATHS[artifact_type]

"""
Collect github projects by programming language
extract trace links between commits and issues
create doc string to source code relationship
"""
import calendar
import logging
import os
import time
from typing import Callable

import git as local_git
from github import Github, Repository
from github.Issue import Issue
from tqdm import tqdm

from data.github.entities.commit import Commit
from data.github.entities.github_artifact_type import GithubArtifactType
from data.github.entities.github_pull import GithubPull
from data.github.entities.repository_artifact_set import RepositoryArtifactSet
from data.github.github_constants import ARTIFACT_PATH, CLONE_PATH, COMMIT_ARTIFACT_FILE, ISSUE_ARTIFACT_FILE, PULL_ARTIFACT_FILE

logger = logging.getLogger(__name__)


class RepositoryDownloader:
    """
    Clones repository and extracts artifacts
    """
    REPO_TEMPLATE = "https://github.com/{}.git"

    def __init__(self, token: str, repository_name: str, clone_dir: str = CLONE_PATH):
        self.token = token
        self.repository_name = repository_name
        self.clone_dir = clone_dir

    def download_repository(self, output_dir: str = ARTIFACT_PATH, load: bool = False):
        """
        Extracts issues, pulls, and commits from repository and saves them in output directory.
        :param output_dir: The path to the directory to save repository artifacts.
        :param load: Whether to load from pre-existing files
        """
        # A. Paths
        output_path = os.path.join(output_dir, self.repository_name)
        issue_file_path = os.path.join(output_path, ISSUE_ARTIFACT_FILE)
        commit_file_path = os.path.join(output_path, COMMIT_ARTIFACT_FILE)
        pull_request_file_path = os.path.join(output_path, PULL_ARTIFACT_FILE)

        # A. Create output directory
        if not os.path.isdir(output_path):
            os.makedirs(output_path)
        git, github_repo, local_repo = self.__get_repo()

        # 1. Parse issues
        issues = self.load_or_parse(issue_file_path, lambda: self.parse_issues(git, github_repo), load)
        pull_requests = self.load_or_parse(pull_request_file_path, lambda: self.parse_pulls(git, github_repo), load)
        commits = self.load_or_parse(commit_file_path, lambda: self.parse_commits(local_repo), load)

        return issues, pull_requests, commits

    @staticmethod
    def load_or_parse(data_file_path: str,
                      artifact_set_creator: Callable[[], RepositoryArtifactSet],
                      load: bool) -> RepositoryArtifactSet:
        """
        Loads or parses artifact set at data file path.
        :param data_file_path: The path to the data file to load.
        :param artifact_set_creator: Callable representing the parsing of an artifact set
        :param load: If true, loads data in data file. Otherwise, calls artifact_set_creator
        :return: Loaded or parsed ArtifactSet
        """
        print("Loading artifacts: ", data_file_path)
        if load:
            artifact_set = RepositoryArtifactSet.load(data_file_path)
        else:
            artifact_set = artifact_set_creator()
            artifact_set.save(data_file_path)
        print("Done!")
        return artifact_set

    def parse_issues(self, github_instance, repo: Repository) -> RepositoryArtifactSet[Issue]:
        """
        Extracts issues at given repository.
        :param github_instance: The instance of the github API.
        :param repo: The repository to gather issues from.
        :return: Set of artifacts representing issues in repository.
        """
        issue_artifacts = []
        for issue in tqdm(repo.get_issues(state="all"), desc="Scraping issues"):
            if issue.pull_request is not None:
                continue
            self.wait_for_rate_limit(github_instance)
            issue_artifacts.append(Issue.parse(issue))

        return RepositoryArtifactSet(issue_artifacts, GithubArtifactType.ISSUE)

    def parse_pulls(self, github_instance, repo: Repository) -> RepositoryArtifactSet[Issue]:
        """
        Extracts pull requests at given repository.
        :param github_instance: The instance of the github API.
        :param repo: The repository to gather pulls from.
        :return: Set of artifacts representing pulls in repository.
        """
        pulls = []
        for pr in tqdm(repo.get_pulls(state="all"), desc="Scraping pulls"):
            self.wait_for_rate_limit(github_instance)
            pulls.append(GithubPull.parse(pr))
        return RepositoryArtifactSet(pulls, GithubArtifactType.PULL_REQUEST)

    @staticmethod
    def parse_commits(repo: Repository) -> RepositoryArtifactSet[Commit]:
        """
        Extracts commits from given local repository.
        :param repo: The repository to gather commits from.
        :return: Set of artifacts representing commits in repository.
        """
        commits = []
        for commit in tqdm(repo.iter_commits(), desc="Parsing commits from repository."):
            try:
                commits.append(Commit.parse_commit(commit))
            except Exception as e:
                print(e)
                print("Commit failed: ", commit.hexsha)
        return RepositoryArtifactSet(commits, GithubArtifactType.COMMIT)

    @staticmethod
    def __clone_repository(repository_name: str, clone_dir: str):
        """
        Clones specified repository into clone directory.
        :param repository_name: The name of the repository to clone (e.g. org/name)
        :param clone_dir: The path to the directory to store clone in.
        :return: None
        """
        repo_url = RepositoryDownloader.REPO_TEMPLATE.format(repository_name)
        clone_path = os.path.join(clone_dir, repository_name)
        if not os.path.exists(clone_path):
            logger.info("Clone {}...".format(repository_name))
            local_git.Repo.clone_from(repo_url, clone_path)
            logger.info("finished cloning project")
        else:
            logger.info("Skip clone project as it already exist...")
        local_repo = local_git.Repo(clone_path)
        return local_repo

    def __get_repo(self) -> Repository:
        """
        Returns github instance for user along with reference to defined repository and its clone.
        :return: github instance, repository, and cloned repository
        """
        github_instance = Github(login_or_token=self.token)
        github_instance.get_user()
        self.wait_for_rate_limit(github_instance)
        repo = github_instance.get_repo(self.repository_name)
        local_repo = self.__clone_repository(self.repository_name, self.clone_dir)
        return github_instance, repo, local_repo

    @staticmethod
    def wait_for_rate_limit(github_instance: Github):
        """
        Checks the current rate limit and waits before expiring if getting close.
        :param github_instance: The github instance with account credentials.
        :return: None
        """
        remaining = github_instance.get_rate_limit().core.remaining
        logger.info("Remaining requests = {}".format(remaining))
        while remaining < 10:
            core_rate_limit = github_instance.get_rate_limit().core
            reset_timestamp = calendar.timegm(core_rate_limit.reset.timetuple())
            sleep_time = reset_timestamp - calendar.timegm(time.gmtime())
            logger.info("Wait untill git core API rate limit reset, reset time = {} seconds".format(sleep_time))
            for i in tqdm(range(sleep_time), desc="Rate Limit Wait"):
                time.sleep(1)
            remaining = github_instance.get_rate_limit().core.remaining

"""
Collect github projects by programming language
extract trace links between commits and issues
create doc string to source code relationship
"""
import calendar
import os
import time
from typing import Callable, List, Union

import git as local_git
from github import Github, Repository
from github.Issue import Issue
from tqdm import tqdm

from data.github.code.cpp_to_header_link_creator import CPPToHeaderLinkCreator
from data.github.gartifacts.gartifact_set import GArtifactSet
from data.github.gartifacts.gartifact_type import GArtifactType
from data.github.gartifacts.gcode_file import GCodeFile
from data.github.gartifacts.gcommit import GCommit
from data.github.gartifacts.gissue import GIssue
from data.github.gartifacts.gpull import GPull
from data.github.github_constants import ALLOWED_CODE_EXTENSIONS, CODE2CODE_ARTIFACT_FILE, CODE_ARTIFACT_FILE, COMMIT_ARTIFACT_FILE, \
    ISSUE_ARTIFACT_FILE, \
    PULL_ARTIFACT_FILE
from util.logging.logger_manager import logger


class RepositoryDownloader:
    """
    Clones repository and extracts artifacts
    """
    REPO_TEMPLATE = "https://github.com/{}.git"

    def __init__(self, token: str, repository_name: str, clone_dir: str):
        """
        Initializes downloader with API token targeting given repository.
        :param token: The API token used for authentication.
        :param repository_name: The name of the github repository.
        :param clone_dir: Path to directory to store repository clone.
        """
        self.token = token
        self.repository_name = repository_name
        self.clone_dir = clone_dir
        self.clone_path = os.path.join(clone_dir, repository_name)
        self.base_path = os.path.join(self.clone_dir, self.repository_name)

    def download_repository(self, output_dir: str, load: bool = False) -> None:
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
        code_export_path = os.path.join(output_path, CODE_ARTIFACT_FILE)
        code2code_export_path = os.path.join(output_path, CODE2CODE_ARTIFACT_FILE)

        # A. Create output directory
        if not os.path.isdir(output_path):
            os.makedirs(output_path)
        git, github_repo, local_repo = self.__get_repo()

        # 1. Parse issues
        self.load_or_retrieve(issue_file_path, lambda: self.parse_issues(git, github_repo), load)
        self.load_or_retrieve(pull_request_file_path, lambda: self.parse_pulls(git, github_repo), load)
        self.load_or_retrieve(commit_file_path, lambda: self.parse_commits(local_repo), load)
        self.load_or_retrieve(code_export_path, lambda: self.read_code_files(), False)
        self.load_or_retrieve(code2code_export_path, lambda: self.extract_code_links(), False)

    @staticmethod
    def load_or_retrieve(data_file_path: Union[str, List[str]],
                         artifact_set_creator: Callable[[], Union[GArtifactSet, List[GArtifactSet]]],
                         load: bool) -> List[GArtifactSet]:
        """
        Loads artifact set or parses artifact set at data file path.
        :param data_file_path: The path to the data file to load.
        :param artifact_set_creator: Callable representing the parsing of an artifact set
        :param load: If true, loads data in data file. Otherwise, calls artifact_set_creator
        :return: Loaded or parsed ArtifactSet
        """
        data_file_paths = data_file_path if isinstance(data_file_path, list) else [data_file_path]
        if load:
            artifact_sets = [GArtifactSet.load(p) for p in data_file_paths]
        else:
            artifact_sets = artifact_set_creator()
            artifact_sets = artifact_sets if isinstance(artifact_sets, list) else [artifact_sets]
            for artifact_set, export_path in zip(artifact_sets, data_file_paths):
                artifact_set.save(export_path)
        return artifact_sets

    def parse_issues(self, github_instance, repo: Repository) -> GArtifactSet[Issue]:
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
            issue_artifacts.append(GIssue.parse(issue))

        return GArtifactSet(issue_artifacts, GArtifactType.ISSUE)

    def parse_pulls(self, github_instance, repo: Repository) -> GArtifactSet[Issue]:
        """
        Extracts pull requests at given repository.
        :param github_instance: The instance of the github API.
        :param repo: The repository to gather pulls from.
        :return: Set of artifacts representing pulls in repository.
        """
        pulls = []
        for pr in tqdm(repo.get_pulls(state="all"), desc="Scraping pulls"):
            self.wait_for_rate_limit(github_instance)
            pulls.append(GPull.parse(pr))
        return GArtifactSet(pulls, GArtifactType.PULL)

    def extract_code_links(self) -> GArtifactSet:
        """
        Find and parse code artifacts in project.
        :return: List containing code artifact set along with set of trace links between code modules.
        """

        cpp_creator = CPPToHeaderLinkCreator.from_dir_path(self.clone_path, self.base_path)
        code_artifacts, code_links = cpp_creator.create_links()

        link_artifact_set = GArtifactSet(list(code_links.values()), GArtifactType.LINK)

        return link_artifact_set

    def read_code_files(self) -> GArtifactSet[GCodeFile]:
        """
        Reads all code files in clone.
        :return: GArtifacSet containing all code files.
        """
        code_artifacts = []
        for subdir, dirs, files in os.walk(self.clone_path):
            for f in files:
                for code_ext in ALLOWED_CODE_EXTENSIONS:
                    if f.endswith(code_ext):
                        file_path = os.path.join(subdir, f)
                        code_artifacts.append(GCodeFile(file_path, self.base_path))
        return GArtifactSet(code_artifacts, GArtifactType.CODE)

    def __get_repo(self) -> Repository:
        """
        Returns github instance for user along with reference to defined repository and its clone.
        :return: github instance, repository, and cloned repository
        """
        github_instance = Github(login_or_token=self.token)
        github_instance.get_user()
        self.wait_for_rate_limit(github_instance)
        repo = github_instance.get_repo(self.repository_name)
        local_repo = self.__clone_repository(self.repository_name, self.clone_path)
        return github_instance, repo, local_repo

    @staticmethod
    def parse_commits(repo: Repository) -> GArtifactSet[GCommit]:
        """
        Extracts commits from given local repository.
        :param repo: The repository to gather commits from.
        :return: Set of artifacts representing commits in repository.
        """
        commits = []
        for commit in tqdm(repo.iter_commits(), desc="Parsing commits from repository."):
            try:
                commits.append(GCommit.parse_commit(commit))
            except Exception as e:
                print(e)
                print("Commit failed: ", commit.hexsha)
        return GArtifactSet(commits, GArtifactType.COMMIT)

    @staticmethod
    def __clone_repository(repository_name: str, clone_path: str):
        """
        Clones specified repository into clone directory.
        :param repository_name: The name of the repository to clone (e.g. org/name)
        :param clone_path: The path to the directory containing cloned repo.
        :return: None
        """
        repo_url = RepositoryDownloader.REPO_TEMPLATE.format(repository_name)
        if not os.path.exists(clone_path):
            logger.info("Clone {}...".format(repository_name))
            local_git.Repo.clone_from(repo_url, clone_path)
            logger.info("finished cloning project")
        else:
            logger.info("Skip clone project as it already exist...")
        local_repo = local_git.Repo(clone_path)
        return local_repo

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

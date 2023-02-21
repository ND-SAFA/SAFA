import os

from data.github.github_repository_exporter import GithubRepositoryExtracter
from data.github.repository_downloader import RepositoryDownloader
from jobs.abstract_job import AbstractJob
from jobs.components.job_args import JobArgs
from jobs.components.job_result import JobResult


class DownloadRepositoryJob(AbstractJob):
    """
    Responsible for downloading repository entities and extracting the artifacts
    and their corresponding trace links from them.
    """

    def __init__(self, job_args: JobArgs, repo_name: str, repo_path: str, clone_path: str, output_path: str, load: bool = False):
        """
        Constructs downloader for repo.
        TODO: Add docs
        TODO: Convert params to object
        TODO: Rename rep_path to artifact_path
        :param repo_name: The GitHub repository ID.
        :param output_path: Path to save repository entities to.
        """
        super().__init__(job_args)
        self.repo_name = repo_name
        self.repo_path = repo_path
        self.clone_path = clone_path
        self.output_path = output_path
        self.load = load
        self.token = os.environ.get("GITHUB_KEY")
        assert self.token is not None, f"Machine has not defined GITHUB_KEY."
        assert self.repo_name is not None, f"Repo id was none."
        assert self.output_path is not None, f"Output path is none."

    def _run(self) -> JobResult:
        repository_downloader = RepositoryDownloader(self.token, self.repo_name, self.clone_path)
        repository_downloader.download_repository(self.repo_path, self.load)

        repo_path = os.path.join(self.repo_path, self.repo_name)
        repository_extracter = GithubRepositoryExtracter(repo_path)
        repository_extracter.extract(self.output_path)
        return JobResult.from_dict({"output_path": self.output_path})

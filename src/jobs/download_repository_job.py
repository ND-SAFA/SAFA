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

    def __init__(self, job_args: JobArgs, repo_id: str, repo_path: str, output_path: str):
        """
        Constructs downloader for repo.
        :param repo_id: The GitHub repository ID.
        :param output_path: Path to save repository entities to.
        """
        super().__init__(job_args)
        self.repo_name = repo_id
        self.repo_path = repo_path
        self.output_path = output_path
        self.token = os.environ.get("GITHUB_KEY")
        assert self.token is not None, f"Machine has not defined GITHUB_KEY."

    def _run(self) -> JobResult:
        repository_downloader = RepositoryDownloader(self.token, self.repo_name)
        repository_downloader.download_repository(self.repo_path)

        repository_extracter = GithubRepositoryExtracter(self.repo_name)
        repository_extracter.extract(self.output_path)

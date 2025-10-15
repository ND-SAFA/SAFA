import os

from gen_common.jobs.abstract_job import AbstractJob
from gen_common.jobs.job_args import JobArgs

from gen.data.github.repository_downloader import RepositoryDownloader
from gen.data.github.repository_exporter import RepositoryExporter


class DownloadRepositoryJob(AbstractJob):
    """
    Responsible for downloading repository entities and extracting the artifacts
    and their corresponding trace links from them.
    """

    def __init__(self, repo_name: str, artifact_store_path: str, clone_path: str, output_path: str, job_args: JobArgs = None,
                 load: bool = False):
        """
        Constructs downloader for repo.
        :param job_args: Job arguments. Current not used.
        :param repo_name: The GitHub repository ID.
        :param artifact_store_path: Path to store repository artifacts to.
        :param clone_path: Path to clone repository into.
        :param output_path: Path to save repository entities to.
        :param load: Whether to load repository from checkpointed files.
        """
        super().__init__(job_args)
        self.repo_name = repo_name
        self.artifact_store_path = artifact_store_path
        self.clone_path = clone_path
        self.output_path = output_path
        self.load = load
        self.token = os.environ.get("GITHUB_KEY")
        assert self.token is not None, f"Machine has not defined GITHUB_KEY."
        assert self.repo_name is not None, f"Repo id was none."
        assert self.output_path is not None, f"Output path is none."

    def _run(self) -> str:
        """
        Downloads or loads repository issues, pulls, and commits exporting processed artifacts to output path.
        :return: JobResult containing empty message.
        """
        repository_downloader = RepositoryDownloader(self.token, self.repo_name, self.clone_path)
        repository_downloader.download_repository(self.artifact_store_path, self.load)

        repo_path = os.path.join(self.artifact_store_path, self.repo_name)
        repository_extracter = RepositoryExporter(repo_path)
        repository_extracter.extract(self.output_path)
        return self.output_path

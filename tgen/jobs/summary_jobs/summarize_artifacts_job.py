from typing import Any, Dict, List

from tgen.common.util.logging.logger_manager import logger
from tgen.data.dataframes.artifact_dataframe import ArtifactKeys
from tgen.data.readers.artifact_project_reader import ArtifactProjectReader
from tgen.jobs.components.args.job_args import JobArgs
from tgen.jobs.summary_jobs.base_summarizer_job import BaseSummarizerJob
from tgen.jobs.summary_jobs.summary_response import SummaryResponse
from tgen.summarizer.summarizer import Summarizer


class SummarizeArtifactsJob(BaseSummarizerJob):
    """
    Handles summarization of artifacts
    """

    def __init__(self, artifacts: List[Dict] = None, artifact_reader: ArtifactProjectReader = None,
                 project_summary_path: str = None, export_dir: str = None, include_project_summary: bool = True,
                 job_args: JobArgs = None, **kwargs):
        """
        Summarizes a given dataset using the given summarizer
        :param artifacts: A dictionary mapping artifact id to a dictionary containing its content
        :param artifact_reader: A reader to read in the artifacts if not provided
        :param project_summary_path: The path to read in a summary
        :param export_dir: The path to save to
        :param job_args: The arguments to the job.
        """
        self.include_project_summary = include_project_summary
        super().__init__(artifacts=artifacts, artifact_reader=artifact_reader,
                         project_summary_path=project_summary_path, export_dir=export_dir, job_args=job_args,
                         do_resummarize_project=include_project_summary,
                         **kwargs)

    def _run(self) -> Dict[Any, str]:
        """
        Performs the summarization of all artifacts and returns the summaries as the new artifact content
        :return: The job result containing all artifacts mapped to their summarized content
        """
        args = self.create_summarizer_args()
        dataset = Summarizer(args).summarize()
        artifacts_df = dataset.artifact_df
        artifacts = artifacts_df.to_dict(orient='index')
        summary = dataset.project_summary if self.include_project_summary else None
        return SummaryResponse(summary=summary, artifacts=artifacts)

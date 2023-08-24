from typing import Any, Dict, List

from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame
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
                 project_summary: str = None, export_dir: str = None, do_resummarize_project: bool = True,
                 is_subset: bool = False, job_args: JobArgs = None, **kwargs):
        """
        Summarizes a given dataset using the given summarizer
        :param artifacts: A dictionary mapping artifact id to a dictionary containing its content
        :param artifact_reader: A reader to read in the artifacts if not provided
        :param project_summary: The summary of the project to use instead of generating a new one
        :param export_dir: The path to save to
        :param is_subset: True if not all of the artifacts are provided
        :param job_args: The arguments to the job.
        """
        self.include_project_summary = do_resummarize_project
        self.is_subset = is_subset
        super().__init__(artifacts=artifacts, artifact_reader=artifact_reader,
                         project_summary=project_summary, export_dir=export_dir, job_args=job_args,
                         do_resummarize_project=do_resummarize_project,
                         **kwargs)

    def _run(self) -> Dict[Any, str]:
        """
        Performs the summarization of all artifacts and returns the summaries as the new artifact content
        :return: The job result containing all artifacts mapped to their summarized content
        """
        args = self.create_summarizer_args()
        if self.is_subset and not self.project_summary:
            summary = None
            artifacts_df = ArtifactDataFrame(self.artifacts)
            artifacts_df.summarize_content(Summarizer.create_summarizer(args))
        else:
            dataset = Summarizer(args).summarize()
            artifacts_df = dataset.artifact_df
            summary = dataset.project_summary if self.include_project_summary else None
        artifacts = artifacts_df.to_dict(orient='records')
        return SummaryResponse(summary=summary, artifacts=artifacts)

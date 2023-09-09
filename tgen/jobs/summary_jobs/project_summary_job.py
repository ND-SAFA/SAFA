from typing import Dict, List

from tgen.common.constants.tracing.ranking_constants import DEFAULT_SUMMARY_TOKENS
from tgen.data.readers.artifact_project_reader import ArtifactProjectReader
from tgen.jobs.components.args.job_args import JobArgs
from tgen.jobs.summary_jobs.base_summarizer_job import BaseSummarizerJob
from tgen.jobs.summary_jobs.summary_response import SummaryResponse
from tgen.models.llm.abstract_llm_manager import AbstractLLMManager
from tgen.summarizer.projects.project_summarizer import ProjectSummarizer
from tgen.summarizer.summarizer import Summarizer


class ProjectSummaryJob(BaseSummarizerJob):

    def __init__(self, artifacts: List[Dict] = None, artifact_reader: ArtifactProjectReader = None,
                 llm_manager: AbstractLLMManager = None, n_tokens: int = DEFAULT_SUMMARY_TOKENS,
                 export_dir: str = None, job_args: JobArgs = None, do_resummarize_project: bool = False, **kwargs):
        """
        Generates a system specification document for containing all artifacts.
        :param artifacts: A dictionary mapping artifact id to a dictionary containing its content
        :param artifact_reader: A reader to read in the artifacts if not provided
        :param llm_manager: The LLM manager in charge of generating the project
        :param n_tokens: The token limit for the LLM
        :param export_dir: The path to save to
        :param job_args: The arguments to the job.
        """
        self.llm_manager: AbstractLLMManager = llm_manager
        self.n_tokens = n_tokens
        kwargs = {"llm_manager_for_project_summary": self.llm_manager, **kwargs} if self.llm_manager else kwargs
        super().__init__(artifacts=artifacts, artifact_reader=artifact_reader, export_dir=export_dir, job_args=job_args, **kwargs)

    def _run(self) -> SummaryResponse:
        """
        Creates specification document and runs.
        :return: System summary.
        """
        args = self.create_summarizer_args()
        summarizer = Summarizer(args)
        summary = ProjectSummarizer(args, self.n_tokens).summarize()
        return SummaryResponse(summary=summary, artifacts=[])

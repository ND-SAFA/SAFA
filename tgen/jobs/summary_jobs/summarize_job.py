from typing import Any, Dict

from tgen.common.util.file_util import FileUtil
from tgen.data.exporters.prompt_dataset_exporter import PromptDatasetExporter
from tgen.data.exporters.safa_exporter import SafaExporter
from tgen.jobs.abstract_job import AbstractJob
from tgen.jobs.components.args.job_args import JobArgs
from tgen.jobs.summary_jobs.summary_response import SummaryResponse
from tgen.summarizer.summarizer import Summarizer
from tgen.summarizer.summarizer_args import SummarizerArgs


class SummarizeJob(AbstractJob):
    """
    Handles summarization of artifacts
    """

    def __init__(self, job_args: JobArgs = None, is_subset: bool = False, **kwargs):
        """
        Summarizes a given dataset using the given summarizer
        :param is_subset: True if not all of the artifacts are provided
        :param job_args: The arguments to the job.
        """
        self.is_subset = is_subset
        self.kwargs = kwargs
        super().__init__(job_args, require_data=True)
        self.args = SummarizerArgs(export_dir=self.job_args.export_dir, **self.kwargs)

    def _run(self) -> Dict[Any, str]:
        """
        Performs the summarization of all artifacts and returns the summaries as the new artifact content
        :return: The job result containing all artifacts mapped to their summarized content
        """
        dataset = self.job_args.dataset
        dataset_dir = self.job_args.dataset_creator.get_project_path() if self.job_args.dataset_creator else None

        self.args.no_project_summary = (self.is_subset and not dataset.project_summary) or self.args.no_project_summary

        summarizer = Summarizer(self.args, dataset=dataset)
        summarized_dataset = summarizer.summarize()

        summary = summarized_dataset.project_summary.to_string() if summarized_dataset.project_summary else None

        if self.args.export_dir or dataset_dir:
            export_dir = FileUtil.safely_join_paths(dataset_dir, self.args.summary_dirname) \
                if dataset_dir else summarizer.state.export_dir
            exporter = PromptDatasetExporter(export_dir,
                                             trace_dataset_exporter_type=SafaExporter,
                                             dataset=summarized_dataset)
            exporter.export()

        artifacts = summarized_dataset.artifact_df.to_artifacts()
        return SummaryResponse(summary=summary, artifacts=artifacts)

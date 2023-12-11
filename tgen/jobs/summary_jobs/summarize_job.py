import os
from typing import Any, Dict

from tgen.common.util.dataclass_util import DataclassUtil
from tgen.common.util.file_util import FileUtil
from tgen.data.creators.prompt_dataset_creator import PromptDatasetCreator
from tgen.data.exporters.prompt_dataset_exporter import PromptDatasetExporter
from tgen.data.exporters.safa_exporter import SafaExporter
from tgen.data.tdatasets.prompt_dataset import PromptDataset
from tgen.jobs.abstract_job import AbstractJob
from tgen.jobs.components.args.job_args import JobArgs
from tgen.jobs.summary_jobs.summary_response import SummaryResponse
from tgen.summarizer.summarizer import Summarizer
from tgen.summarizer.summarizer_args import SummarizerArgs


class SummarizeJob(AbstractJob):
    """
    Handles summarization of artifacts
    """

    def __init__(self, dataset: PromptDataset = None, dataset_creator: PromptDatasetCreator = None, export_dir: str = None,
                 is_subset: bool = False, job_args: JobArgs = None, **kwargs):
        """
        Summarizes a given dataset using the given summarizer
        :param dataset: The dataset to summarize.
        :param dataset_creator: Creates the dataset to summarize if one is not provided
        :param export_dir: The path to save to
        :param is_subset: True if not all of the artifacts are provided
        :param job_args: The arguments to the job.
        """
        self.is_subset = is_subset
        self.export_dir = export_dir
        self.dataset = dataset
        self.dataset_creator = dataset_creator
        self.kwargs = kwargs
        self.args = SummarizerArgs(export_dir=export_dir,
                                   **self.kwargs)
        super().__init__(job_args)

    def _run(self) -> Dict[Any, str]:
        """
        Performs the summarization of all artifacts and returns the summaries as the new artifact content
        :return: The job result containing all artifacts mapped to their summarized content
        """
        dataset: PromptDataset = DataclassUtil.post_initialize_datasets(self.dataset, self.dataset_creator)
        dataset_dir = self.dataset_creator.get_project_path() if self.dataset_creator else None

        self.args.no_project_summary = self.is_subset and not dataset.project_summary

        summarizer = Summarizer(self.args, dataset=dataset)
        dataset = summarizer.summarize()

        summary = dataset.project_summary.to_string() if dataset.project_summary else None

        if self.args.export_dir or dataset_dir:
            export_dir = FileUtil.safely_join_paths(dataset_dir, self.args.summary_dirname) \
                if dataset_dir else summarizer.state.export_dir
            exporter = PromptDatasetExporter(os.path.join(export_dir, "final_dataset"),
                                             trace_dataset_exporter_type=SafaExporter,
                                             dataset=dataset)
            exporter.export()

        artifacts = dataset.artifact_df.to_artifacts()
        return SummaryResponse(summary=summary, artifacts=artifacts)

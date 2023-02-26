import os

from data.creators.trace_dataset_creator import TraceDatasetCreator
from data.exporters.safa_exporter import SafaExporter
from jobs.abstract_job import AbstractJob
from jobs.components.job_args import JobArgs
from jobs.components.job_result import JobResult


class ExportDatasetJob(AbstractJob):
    """
    Converts any format of trace dataset creator to SAFA format.
    """

    def __init__(self, trace_dataset_creator: TraceDatasetCreator, export_path: str, job_args: JobArgs = None):
        """
        Responsible for creating and saving new data
        :param trace_dataset_creator: The trace dataset to export.
        """
        if job_args is None:
            job_args = JobArgs()
        super().__init__(job_args=job_args)
        self.trace_dataset_creator = trace_dataset_creator
        self.export_path = export_path

    def _run(self, **kwargs) -> JobResult:
        """
        Creates and saves the data
        :return: job results including location of saved data
        """
        os.makedirs(self.export_path, exist_ok=True)
        trace_dataset = self.trace_dataset_creator.create()
        artifact_df, trace_df, layer_mapping_df = self.trace_dataset_creator.project_reader.read_project()
        safa_exporter = SafaExporter()
        safa_exporter.export(self.export_path, trace_dataset.links, artifact_df, layer_mapping_df)
        return JobResult.from_dict({"status": 0, JobResult.SAVED_DATASET_PATHS: self.export_path})

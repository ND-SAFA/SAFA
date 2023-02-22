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

    def __init__(self, trace_dataset_creator: TraceDatasetCreator, export_path: str):
        """
        Responsible for creating and saving new data
        :param trace_dataset_creator: The trace dataset to export.
        """
        super().__init__(job_args=JobArgs())
        self.trace_dataset_creator = trace_dataset_creator
        self.export_path = export_path

    def _run(self, **kwargs) -> JobResult:
        """
        Creates and saves the data
        :return: job results including location of saved data
        """
        os.makedirs(self.export_path, exist_ok=True)
        safa_exporter = SafaExporter(self.trace_dataset_creator)
        safa_exporter.export(self.export_path)
        return JobResult.from_dict({"status": 0, "msg": f"Project exported to:{safa_exporter.export_path}"})

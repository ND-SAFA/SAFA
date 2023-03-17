from typing import Type

from data.exporters.abstract_dataset_exporter import AbstractDatasetExporter
from data.exporters.supported_exporters import SupportedExporters
from jobs.abstract_job import AbstractJob
from jobs.components.job_args import JobArgs
from jobs.components.job_result import JobResult
from util.base_object import BaseObject
from util.override import overrides


class ExportDatasetJob(AbstractJob):
    """
    Converts any format of trace dataset creator to SAFA format.
    """

    def __init__(self, exporter: AbstractDatasetExporter, job_args: JobArgs = None):
        """
        Responsible for creating and saving new data
        :param exporter: The exporter to use to save the dataset
        :param job_args: The args for the job
        """
        if job_args is None:
            job_args = JobArgs()
        super().__init__(job_args=job_args)
        self.exporter = exporter

    def _run(self, **kwargs) -> JobResult:
        """
        Creates and saves the data
        :return: job results including location of saved data
        """
        self.exporter.export()
        return JobResult.from_dict({"status": 0, JobResult.SAVED_DATASET_PATHS: self.exporter.export_path})

    @classmethod
    @overrides(BaseObject)
    def _get_child_enum_class(cls, abstract_class: Type, child_class_name: str) -> Type:
        """
        Returns the correct enum class mapping name to class given the abstract parent class type and name of child class
        :param abstract_class: the abstract parent class type
        :param child_class_name: the name of the child class
        :return: the enum class mapping name to class
        """
        return SupportedExporters

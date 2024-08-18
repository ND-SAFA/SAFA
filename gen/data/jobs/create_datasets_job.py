from typing import List

from gen_common.data.exporters.supported_dataset_exporters import SupportedDatasetExporter
from gen_common.data.managers.trainer_dataset_manager import TrainerDatasetManager
from gen_common.jobs.abstract_job import AbstractJob
from gen_common.jobs.job_args import JobArgs


class CreateDatasetsJob(AbstractJob):

    def __init__(self, trainer_dataset_manager: TrainerDatasetManager, job_args: JobArgs = None,
                 format_type: SupportedDatasetExporter = SupportedDatasetExporter.CSV):
        """
        Responsible for creating and saving new data
        :param job_args: the arguments for the job
        :param trainer_dataset_manager: manages all datasets for the trainer
        :param format_type: The format to export the data as.
        """
        super().__init__(job_args=job_args)
        assert job_args.export_dir, "Must specify a directory to save datasets to but export_dir is not provided. "
        self.trainer_dataset_manager = trainer_dataset_manager
        self.format_type = format_type

    def _run(self, **kwargs) -> List[str]:
        """
        Creates and saves the data
        :return: job results including location of saved data
        """
        saved_dataset_paths = self.trainer_dataset_manager.export_dataset_splits(self.job_args.export_dir, self.format_type)
        assert len(saved_dataset_paths) > 0, "Either unable to save data or no data creators were provided"
        return saved_dataset_paths

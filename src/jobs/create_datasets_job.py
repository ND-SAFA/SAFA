from typing import Dict, Any

from data.datasets.managers.trainer_dataset_manager import TrainerDatasetManager
from jobs.abstract_job import AbstractJob
from jobs.components.job_args import JobArgs
from jobs.components.job_result import JobResult


class CreateDatasetsJob(AbstractJob):

    def __init__(self, job_args: JobArgs, trainer_dataset_manager: TrainerDatasetManager):
        """
        Responsible for creating and saving new data
        :param job_args: the arguments for the job
        :param trainer_dataset_manager: manages all datasets for the trainer
        """
        job_args.save_dataset_splits = True
        super().__init__(job_args=job_args)
        self.trainer_dataset_manager = trainer_dataset_manager

    def _run(self, **kwargs) -> JobResult:
        """
        Creates and saves the data
        :return: job results including location of saved data
        """
        saved_dataset_paths = self.trainer_dataset_manager.save_dataset_splits(self.job_args.output_dir)
        assert len(saved_dataset_paths) > 0, "Either unable to save data or no data creators were provided"
        return JobResult.from_dict({JobResult.SAVED_DATASET_PATHS: saved_dataset_paths})

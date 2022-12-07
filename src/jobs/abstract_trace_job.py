from abc import ABC

from data.datasets.trainer_dataset_manager import TrainerDatasetManager
from jobs.abstract_job import AbstractJob
from jobs.components.job_args import JobArgs
from models.model_manager import ModelManager
from train.trace_trainer import TraceTrainer
from train.trainer_args import TrainerArgs


class AbstractTraceJob(AbstractJob, ABC):

    def __init__(self, job_args: JobArgs, model_manager: ModelManager,
                 trainer_dataset_manager: TrainerDatasetManager, trainer_args: TrainerArgs):
        """
        The base job class for tracing jobs
        :param job_args: the arguments for the job
        :param model_manager: the manages the model necessary for the job
        :param trainer_dataset_manager: manages all datasets for the trainer
        :param trainer_args: other arguments needed for the trainer
        """
        super().__init__(job_args=job_args, model_manager=model_manager)
        self.trainer_args = trainer_args
        self.trainer_dataset_manager = trainer_dataset_manager
        self.saved_dataset_paths = self.trainer_dataset_manager.save_dataset_splits(job_args.output_dir) \
            if job_args.save_dataset_splits else []
        self._trainer = None

    def get_trainer(self, **kwargs) -> TraceTrainer:
        """
        Gets the trace trainer for the job
        :param kwargs: any additional parameters for the trainer
        :return: the trainer
        """
        if self._trainer is None:
            self._trainer = TraceTrainer(trainer_args=self.trainer_args, trainer_dataset_manager=self.trainer_dataset_manager,
                                         model_manager=self.model_manager, **kwargs)
        return self._trainer

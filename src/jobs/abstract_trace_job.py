from abc import ABC

from jobs.abstract_job import AbstractJob
from jobs.components.job_args import JobArgs
from train.trace_trainer import TraceTrainer


class AbstractTraceJob(AbstractJob, ABC):

    def __init__(self, job_args: JobArgs):
        """
        The base job class for tracing jobs
        """
        job_args.model_path = job_args.model_path
        super().__init__(job_args)
        self.trainer_args = job_args.trainer_args
        self.saved_dataset_paths = self.trainer_args.trainer_dataset_container.save_dataset_splits(job_args.output_dir) \
            if self.trainer_args.save_dataset_splits else []
        self._trainer = None

    def _create_trace_args(self):
        pass

    def _create_dataset_container(self):
        pass

    def get_trainer(self, **kwargs) -> TraceTrainer:
        """
        Gets the trace trainer for the job
        :param kwargs: any additional parameters for the trainer
        :return: the trainer
        """
        if self._trainer is None:
            self._trainer = TraceTrainer(args=self.job_args.trainer_args, model_manager=self.get_model_manager(),
                                         **kwargs)
        return self._trainer

import os
import uuid
from copy import deepcopy
from typing import List

from experiments.experiment_step import ExperimentStep
from jobs.abstract_job import AbstractJob
from jobs.components.job_result import JobResult
from jobs.train_job import TrainJob


class MultiEpochExperimentStep(ExperimentStep):

    def run(self, output_dir: str, jobs_for_undetermined_vars: List[AbstractJob] = None) -> List[AbstractJob]:
        """
        Runs a job for each epoch in the trainer_args.train_epochs_range
        :param output_dir: the base output dir for the step
        :param jobs_for_undetermined_vars: job used to fill in any undetermined vars
        :return: the best job
        """
        orig_job: TrainJob = self.jobs.pop()
        epochs = [i for i in range(*orig_job.trainer_args.train_epochs_range)]
        orig_job.trainer_args.train_epochs_range = None
        self.jobs = self._construct_epoch_jobs(epochs, orig_job)
        return super().run(output_dir, jobs_for_undetermined_vars)

    @staticmethod
    def _construct_epoch_jobs(epochs: List[int], orig_job: TrainJob) -> List[AbstractJob]:
        """
        Constructs the jobs for each epoch
        :param epochs: the list of all epochs
        :param orig_job: the original train job
        :return: the list of jobs for each epoch
        """
        jobs = []
        for i, epoch_total in enumerate(epochs):
            prev_epoch = epochs[i - 1] if (i - 1) >= 0 else None
            epoch_job = deepcopy(orig_job)
            epoch_job.id = str(uuid.uuid4())
            epoch_job.trainer_args.num_train_epochs = epoch_total
            epoch_job.result[JobResult.EXPERIMENTAL_VARS]["num_train_epochs"] = epoch_total
            epoch_job.trainer_args.total_training_epochs = epoch_total

            # Set model paths
            model_checkpoint_path = os.path.join(orig_job.model_manager.model_output_path, str(orig_job.id))
            if prev_epoch:
                epoch_job.model_manager.model_path = model_checkpoint_path
                epoch_job.trainer_args.checkpoint_path = model_checkpoint_path
            epoch_job.model_manager.model_output_path = model_checkpoint_path
            jobs.append(epoch_job)
        return jobs

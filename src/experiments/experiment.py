import os
import uuid
from typing import List

from experiments.experiment_step import ExperimentStep
from jobs.abstract_job import AbstractJob
from util.base_object import BaseObject
from util.file_util import FileUtil
from util.logging.logger_config import LoggerConfig
from util.logging.logger_manager import LoggerManager
from util.status import Status


class Experiment(BaseObject):
    _STEP_DIR_NAME = "step_%s"

    def __init__(self, steps: List[ExperimentStep], output_dir: str, logger_config: LoggerConfig = LoggerConfig()):
        """
        Represents an experiment run
        :param steps: List of all experiment steps to run
        :param output_dir: The path to save output to
        :param logger_config: Configures the logging for the project
        """
        self.id = uuid.uuid4()
        self.steps = steps
        self.output_dir = output_dir
        FileUtil.create_dir_safely(output_dir)
        self.logger_config = logger_config
        self._setup_logger()
        self._update_step_paths()

    def run(self):
        """
        Runs all steps in the experiment
        :return: None
        """
        jobs_for_undetermined_vals = None
        for i, step in enumerate(self.steps):
            step_output_dir = os.path.join(self.output_dir, str(self.id), self._STEP_DIR_NAME % i)
            jobs_for_undetermined_vals = step.run(step_output_dir, jobs_for_undetermined_vals)
            if step.status == Status.FAILURE:
                break

    def get_all_jobs(self) -> List[AbstractJob]:
        """
        Returns a list of all jobs across all steps
        :return: a list of all jobs across all steps
        """
        jobs = []
        for step in self.steps:
            jobs.extend(step.jobs)
        return jobs

    def _update_step_paths(self) -> None:
        """
        Updates the experiment directory of given steps.
        :return: None
        """
        for step in self.steps:
            step.experiment_dir = self.output_dir

    def _setup_logger(self) -> None:
        """
        Setups the logger for the experiment
        :return: None
        """
        if self.logger_config.output_dir is None:
            self.logger_config.output_dir = self.output_dir
        LoggerManager.configure_logger(self.logger_config)

    def _get_step_output_path(self, step_num: int) -> str:
        """
        Gets the output path for the step
        :param step_num: the number of the step
        :return: the output path
        """
        return os.path.join(self.output_dir, str(self.id), self._STEP_DIR_NAME.format(step_num))

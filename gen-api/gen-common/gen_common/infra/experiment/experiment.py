import os
import uuid
from typing import List

from gen_common.constants.experiment_constants import EXPERIMENT_ID_DEFAULT
from gen_common.infra.base_object import BaseObject
from gen_common.infra.experiment.experiment_step import ExperimentStep
from gen_common.infra.t_logging.logger_config import LoggerConfig
from gen_common.infra.t_logging.logger_manager import LoggerManager
from gen_common.jobs.abstract_job import AbstractJob
from gen_common.util.file_util import FileUtil
from gen_common.util.status import Status


class Experiment(BaseObject):
    _STEP_DIR_NAME = "step_%s"
    _EXPERIMENT_DIR_NAME = "experiment_%s"

    def __init__(self, steps: List[ExperimentStep], output_dir: str, logger_config: LoggerConfig = LoggerConfig(),
                 experiment_id: int = EXPERIMENT_ID_DEFAULT, delete_prev_experiment_dir: bool = False):
        """
        Represents an experiment run
        :param steps: List of all experiment steps to run
        :param output_dir: The path to save output to
        :param logger_config: Configures the logging for the project
        :param experiment_id: The id (or index) of the experiment being run. Used for creating readable output directories.
        :param delete_prev_experiment_dir: If True, removes the previous experiment dir if it exists
        """
        self.id = uuid.uuid4()
        self.steps = steps
        self.output_dir = output_dir
        FileUtil.create_dir_safely(output_dir)
        self.logger_config = logger_config
        self._setup_logger()
        self.experiment_index = experiment_id
        self.delete_prev_experiment_dir = delete_prev_experiment_dir
        self.status = Status.NOT_STARTED

    def run(self) -> List[AbstractJob]:
        """
        Runs all steps in the experiment
        :return: None
        """
        self.status = Status.IN_PROGRESS
        jobs_for_undetermined_vals = []
        for i, step in enumerate(self.steps):
            step_output_dir = self.get_step_output_dir(self.experiment_index, i)
            jobs_for_undetermined_vals.extend(step.run(step_output_dir, jobs_for_undetermined_vals))
            if step.status == Status.FAILURE:
                self.status = Status.FAILURE
                break
        self.status = Status.SUCCESS
        return jobs_for_undetermined_vals

    def get_all_jobs(self) -> List[AbstractJob]:
        """
        Returns a list of all jobs across all steps
        :return: a list of all jobs across all steps
        """
        jobs = []
        for step in self.steps:
            jobs.extend(step.jobs)
        return jobs

    def _setup_logger(self) -> None:
        """
        Setups the logger for the experiment
        :return: None
        """
        if self.logger_config.output_dir is None:
            self.logger_config.output_dir = self.output_dir
        LoggerManager.configure_logger(self.logger_config)

    def get_step_output_dir(self, experiment_id: int, step_id: int) -> str:
        """
        Returns the output path of the step from base directory.
        :param experiment_id: The id or index of the step.
        :param step_id: The id or index of the step.
        :return: Step's output path.
        """
        return os.path.join(self.output_dir, Experiment._EXPERIMENT_DIR_NAME % experiment_id, Experiment._STEP_DIR_NAME % step_id)

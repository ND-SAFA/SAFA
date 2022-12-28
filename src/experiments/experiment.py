import os
from typing import List

from experiments.experiment_step import ExperimentStep
from util.base_object import BaseObject
from util.file_util import FileUtil


class Experiment(BaseObject):

    _STEP_DIR_NAME = "step_{}"

    def __init__(self, steps: List[ExperimentStep], output_dir: str):
        """
        Represents an experiment run
        :param steps: list of all experiment steps to run
        """
        self.steps = steps
        self.output_dir = output_dir
        FileUtil.make_dir_safe(output_dir)

    def run(self):
        """
        Runs all steps in the experiment
        :return: None
        """
        jobs_for_undetermined_vals = None
        for i, step in enumerate(self.steps):
            jobs_for_undetermined_vals = step.run(jobs_for_undetermined_vals)
            step.save_results(self._get_step_output_path(i))

    def _get_step_output_path(self, step_num: int) -> str:
        """
        Gets the output path for the step
        :param step_num: the number of the step
        :return: the output path
        """
        return os.path.join(self.output_dir, self._STEP_DIR_NAME.format(step_num))

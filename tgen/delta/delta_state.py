import os
from copy import deepcopy
from dataclasses import dataclass, field

from typing import List, Dict, Set

from tgen.common.util.file_util import FileUtil
from tgen.common.util.logging.logger_manager import logger
from tgen.constants.deliminator_constants import COMMA, DASH
from tgen.data.processing.cleaning.separate_joined_words_step import SeparateJoinedWordsStep
from tgen.state.state import State


@dataclass
class DeltaState(State):
    export_dir: str = None  # The path to save the state to

    project_summary: str = None  # The summary of the project

    diff_summaries: Dict = None  # maps filename to the results of the diff summary

    change_summary_output: Dict = None  # output from model, includes the grouping of changes and summaries

    change_summary: str = None # Markdown version of the change summary

    def on_step_complete(self, step_name: str) -> None:
        """
        Performs all tasks required after step complete (i.e. saving)
        :param step_name: The name of the step completed
        :return: None
        """
        super().on_step_complete(step_name)
        self.save(step_name)

    @staticmethod
    def load_latest(load_dir: str, steps: List) -> "DeltaState":
        """
        Loads the latest state found in the load dir
        :param load_dir: The directory to load the state from
        :param steps: The delta steps
        :return: The loaded state
        """
        steps = deepcopy(steps)
        steps.reverse()
        for step in steps:
            path = os.path.join(load_dir, DeltaState._get_filename(step.__name__))
            if os.path.exists(path):
                attrs = FileUtil.read_yaml(path)
                logger.info(f"Loaded previous state from {path}")
                return DeltaState(**attrs)
        logger.warning(f"No previous state was found at {load_dir}. Creating new state.")
        return DeltaState()

    def save(self, step_name: str) -> bool:
        """
        Saves the current state
        :param step_name: The step name that the pipeline is currently at
        :return: True if saved successfully else False
        """
        if self.export_dir is None:
            return False

        try:
            save_path = os.path.join(self.export_dir, self._get_filename(step_name))
            FileUtil.write_yaml(vars(self), save_path)
            logger.info(f"Saved state to {save_path}")
            return True
        except Exception:
            logger.exception("Unable to save current state.")
            return False

    @staticmethod
    def _get_filename(step_name: str) -> str:
        """
        Returns the filename for the given step
        :param step_name: The name of the step
        :return: The filename for the given step
        """
        step_name = DASH.join(SeparateJoinedWordsStep.separate_camel_case_word(step_name)).lower()
        return f"state-{step_name}.yaml"

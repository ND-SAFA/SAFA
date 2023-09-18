import os
from collections.abc import Set
from copy import deepcopy
from dataclasses import dataclass, field
from typing import Any, List, Union, Dict

from tgen.common.util.base_object import BaseObject
from tgen.common.util.file_util import FileUtil
from tgen.common.util.logging.logger_manager import logger
from tgen.common.util.param_specs import ParamSpecs
from tgen.common.util.reflection_util import ReflectionUtil
from tgen.common.util.yaml_util import YamlUtil
from tgen.common.constants.deliminator_constants import DASH, EMPTY_STRING
from tgen.data.creators.abstract_dataset_creator import AbstractDatasetCreator
from tgen.data.processing.cleaning.separate_joined_words_step import SeparateJoinedWordsStep
from tgen.data.tdatasets.prompt_dataset import PromptDataset
from tgen.data.tdatasets.trace_dataset import TraceDataset


@dataclass
class State(BaseObject):
    """
    Represents a state of an object in time
    """

    completed_steps: Union[set, list, dict] = field(default_factory=dict)

    export_dir: str = EMPTY_STRING

    _checkpoint_dir: str = "state_checkpoints"

    def __post_init__(self):
        """
        Performs any operations after initialization
        :return: None
        """
        if not isinstance(self.completed_steps, Dict):
            self.completed_steps = {step_name: 1 for step_name in self.completed_steps}

    def step_is_complete(self, step_name: str) -> bool:
        """
        Checks whether the step is complete
        :param step_name: The name of the step completed
        :return: True if the step was already completed
        """
        return step_name in self.completed_steps

    def mark_step_as_incomplete(self, step_name: str) -> None:
        """
        Removes step from completed steps
        :param step_name: The name of the step to mark as incomplete
        :return: None
        """
        if not self.step_is_complete(step_name):
            return
        self.completed_steps.pop(step_name)

    def mark_step_as_complete(self, step_name: str) -> None:
        """
        Adds step to completed steps and increments the number of times it was run
        :param step_name: The name of the step to mark as complete
        :return: None
        """
        if step_name not in self.completed_steps:
            self.completed_steps[step_name] = 0
        self.completed_steps[step_name] += 1

    def on_step_complete(self, step_name: str) -> None:
        """
        Performs all tasks required after step complete
        :param step_name: The name of the step completed
        :return: None
        """
        self.mark_step_as_complete(step_name)
        self.save(step_name, run_num=self.completed_steps[step_name])

    def save(self, step_name: str, run_num: int = 1) -> bool:
        """
        Saves the current state
        :param step_name: The step name that the pipeline is currently at
        :param run_num: The number of times the step has been run
        :return: True if saved successfully else False
        """
        if not self.export_dir:
            return False

        try:
            save_path = self._get_path_to_state_checkpoint(self.export_dir, step_name, run_num)
            as_dict = {k: (v.as_creator(self._get_path_to_state_checkpoint(self.export_dir), k)
                           if isinstance(v, PromptDataset) or isinstance(v, TraceDataset) else v) for k, v in vars(self).items()}
            YamlUtil.write(as_dict, save_path)
            logger.info(f"Saved state to {save_path}")
            return True
        except Exception:
            logger.exception("Unable to save current state.")
            return False

    @classmethod
    def load_latest(cls, load_dir: str, step_names: List[str]) -> "State":
        """
        Loads the latest state found in the load dir
        :param load_dir: The directory to load the state from
        :param step_names: The names of the steps
        :return: The loaded state
        """
        steps = deepcopy(step_names)
        steps.reverse()
        try:
            for step in steps:
                path = cls._get_path_to_state_checkpoint(load_dir, step)
                if os.path.exists(path):
                    state = cls.load_state_from_path(path, raise_exception=True)
                    return state
            raise FileNotFoundError(f"Unable to find a previous state to load from {load_dir}")
        except Exception:
            logger.exception(f"Could not reload state of step: {step}. Creating new instance.")
            return cls()

    @classmethod
    def load_state_from_path(cls, path: str, raise_exception: bool = False) -> Union["State", Exception]:
        """
        Loads the state from a given path
        :param path: The path to load the state from
        :param raise_exception: If True, raises an exception if loading false else just returns exception
        :return: The state instance if success, else the exception
        """
        try:
            logger.info(f"Reading step state: {path}")
            param_specs = ParamSpecs.create_from_method(cls.__init__)
            attrs = {name: cls._check_type(name, val, param_specs) for name, val in YamlUtil.read(path).items()}
            obj = cls(**attrs)
            logger.info(f"Loaded previous state from {path}")
            return obj
        except Exception as e:
            if raise_exception:
                raise e
            return e

    @classmethod
    def _check_type(cls, name: str, val: Any, param_specs: ParamSpecs) -> Any:
        """
        Checks the type of the value to ensure that it is the expected type
        :param name: The name of the attribute
        :param val: The value of the attribute
        :param param_specs: Specifies the expected types
        :return: The value as correct type or raises exception
        """
        expected_param_type = param_specs.param_types.get(name)
        if isinstance(val, AbstractDatasetCreator) and not ReflectionUtil.is_type(val, expected_param_type, name,
                                                                                  print_on_error=False):
            val = val.create()
        if not ReflectionUtil.is_type(val, expected_param_type, name):
            raise TypeError(f"Expected {name} to be {expected_param_type} but was type {type(val)}")
        return val

    @staticmethod
    def _get_path_to_state_checkpoint(directory: str, step_name: str = EMPTY_STRING, run_num: int = 1) -> str:
        """
        Gets the path to the checkpoint for the state corresponding to the given step name
        :param directory: The directory that the checkpoints live in
        :param step_name: The name of the step that corresponds with the desired state
        :param run_num: The number of times the step has been run
        :return: The path to the checkpoint for the state corresponding to the given step name
        """
        if os.path.split(directory)[-1] != State._checkpoint_dir:
            directory = os.path.join(directory, State._checkpoint_dir)
        FileUtil.create_dir_safely(directory)
        if not step_name:
            return directory
        return os.path.join(directory, State._get_filename(step_name, run_num))

    @staticmethod
    def _get_filename(step: Any, run_num: int = 1) -> str:
        """
        Returns the filename for the given step
        :param step: The name of the step
        :param run_num: The number of times the step has been run
        :return: The filename for the given step
        """
        step = DASH.join(SeparateJoinedWordsStep.separate_camel_case_word(step)).lower()
        if run_num > 1:
            step = f"{step}-{run_num}"
        return f"state-{step}.yaml"

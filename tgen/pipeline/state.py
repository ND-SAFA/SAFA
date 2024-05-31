import os
from collections.abc import Set
from copy import deepcopy
from dataclasses import dataclass, field
from typing import Any, Dict, List, Union, Optional

from tgen.common.constants.deliminator_constants import DASH, EMPTY_STRING, UNDERSCORE
from tgen.common.logging.logger_manager import logger
from tgen.common.util.base_object import BaseObject
from tgen.common.util.enum_util import EnumUtil
from tgen.common.util.file_util import FileUtil
from tgen.common.util.param_specs import ParamSpecs
from tgen.common.util.reflection_util import ReflectionUtil
from tgen.common.util.status import Status
from tgen.common.util.yaml_util import YamlUtil
from tgen.data.processing.cleaning.separate_joined_words_step import SeparateJoinedWordsStep
from tgen.summarizer.summary import Summary


@dataclass
class State(BaseObject):
    """
    Represents a state of an object in time
    """

    completed_steps: Union[set, list, dict] = field(default_factory=dict)

    export_dir: str = EMPTY_STRING

    project_summary: Summary = None

    total_input_cost: float = 0

    total_output_cost: float = 0

    _CHECKPOINT_DIRNAME: str = "state_checkpoints"

    _PATH_TERMS = {"path", "dir", "directory"}

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
        self.save(step_name=step_name, run_num=self.completed_steps[step_name])

    def save(self, step_name: str, run_num: int = 1, attrs2ignore: Set = None) -> bool:
        """
        Saves the current state
        :param step_name: The step name that the pipeline is currently at
        :param run_num: The number of times the step has been run
        :param attrs2ignore: The attributes to ignore when saving
        :return: True if saved successfully else False
        """
        if not self.export_dir:
            return False

        try:
            logger.info(f"Saving state for {step_name}")
            step_num = len(self.completed_steps) \
                if not EnumUtil.get_enum_from_name(Status, step_name.upper(), raise_exception=False) else None
            save_path = self.get_path_to_state_checkpoint(self.export_dir, step_name, run_num, step_num)
            as_dict = {k: v for k, v in vars(self).items() if not attrs2ignore or k not in attrs2ignore}
            collapsed_paths = self.collapse_or_expand_paths(as_dict)
            YamlUtil.write(collapsed_paths, save_path)
            logger.info(f"Saved state to {save_path}")
            return True
        except Exception as e:
            logger.exception("Unable to save current state.")
            return False

    @classmethod
    def delete_state_files(cls, load_dir: str, step_names: List[str], step_to_delete_from: str = None) -> None:
        """
        Deletes all state files starting at the step to delete from
        :param load_dir: The directory to delete the state from
        :param step_names: The names of the steps
        :param step_to_delete_from: The name of the step, from which all later states will be deleted
        :return: None
        """
        step_index = step_names.index(step_to_delete_from) if step_to_delete_from else 0
        for i, step in enumerate(step_names[step_index:]):
            delete_path = cls.get_path_to_state_checkpoint(load_dir, step, step_num=step_index + i + 1)
            FileUtil.delete_file_safely(delete_path)

    @classmethod
    def collapse_or_expand_paths(cls, as_dict: Dict, collapse: bool = True) -> Dict:
        """
        Collapses or expands all path variables in the dictionary of vars
        :param as_dict: The vars dictionary
        :param collapse: If True, collapses the path
        :return: The dictionary with collapsed or expanded paths
        """
        method = FileUtil.collapse_paths if collapse else FileUtil.expand_paths
        output = {}
        for k, v in as_dict.items():
            is_path = not ReflectionUtil.is_function(v) and cls._is_a_path_variable(k)
            output[k] = method(v) if is_path else v
        return output

    @classmethod
    def load_latest(cls, load_dir: str, step_names: List[str], log_exception: bool = True) -> "State":
        """
        Loads the latest state found in the load dir
        :param load_dir: The directory to load the state from
        :param step_names: The names of the steps
        :param log_exception: If True, logs any exceptions that occur, else fails silently
        :return: The loaded state
        """
        steps = deepcopy(step_names)
        steps.reverse()
        try:
            for i, step in enumerate(steps):
                path = cls.get_path_to_state_checkpoint(load_dir, step, step_num=len(step_names) - i)
                if os.path.exists(path):
                    state = cls.load_state_from_path(path, raise_exception=True)
                    return state
            raise FileNotFoundError(f"Unable to find a previous state to load from {load_dir}")
        except FileNotFoundError as f:
            if log_exception:
                logger.info(str(f))
        except Exception:
            if log_exception:
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
            expanded_paths = cls.collapse_or_expand_paths(attrs, collapse=False)
            obj = cls(**expanded_paths)
            logger.info(f"Loaded previous state from {path}")
            return obj
        except Exception as e:
            if raise_exception or True:
                raise e
            return e

    def update_total_costs_from_state(self, other_state: "State") -> None:
        """
        Updates the total costs by combining current costs with those accumulated in the othhr state
        :param other_state: The state to combine costs with
        :return: None
        """
        self.total_input_cost += other_state.total_input_cost
        self.total_output_cost += other_state.total_output_cost

    def get_total_costs(self) -> float:
        """
        Gets the combined cost of input and output tokens
        :return: The combined cost of input and output tokens
        """
        return self.total_output_cost + self.total_input_cost

    @staticmethod
    def _is_a_path_variable(varname: str) -> bool:
        """
        Returns True if the variable name contains a path term, suggesting it is intended to be a a path
        :param varname: The variable name
        :return: True if it contains a path term
        """
        snake_case_separated = varname.split(UNDERSCORE)
        for path_term in State._PATH_TERMS:
            if path_term in snake_case_separated:
                return True
        return False

    @classmethod
    def _check_type(cls, name: str, val: Any, param_specs: ParamSpecs) -> Any:
        """
        Checks the type of the value to ensure that it is the expected type
        :param name: The name of the attribute
        :param val: The value of the attribute
        :param param_specs: Specifies the expected types
        :return: The value as correct type or raises exception
        """
        if name not in param_specs.param_names:
            raise Exception(f"Unknown parameter {name} in {cls.__name__}")
        expected_param_type = param_specs.param_types.get(name, Any)
        if not ReflectionUtil.is_type(val, expected_param_type, name, print_on_error=False):
            val = cls._try_convert_from_yaml(name, val, param_specs, expected_param_type)
            if val is None:
                raise TypeError(f"Expected {name} to be {expected_param_type} but was type {type(val)}")
        return val

    @staticmethod
    def get_path_to_state_checkpoint(directory: str, step_name: str = EMPTY_STRING, run_num: int = 1,
                                     step_num: int = None) -> str:
        """
        Gets the path to the checkpoint for the state corresponding to the given step name
        :param directory: The directory that the checkpoints live in
        :param step_name: The name of the step that corresponds with the desired state
        :param run_num: The number of times the step has been run
        :param step_num: The number of the step being run
        :return: The path to the checkpoint for the state corresponding to the given step name
        """
        if os.path.split(directory)[-1] != State._CHECKPOINT_DIRNAME:
            directory = os.path.join(directory, State._CHECKPOINT_DIRNAME)
        FileUtil.create_dir_safely(directory)
        if not step_name:
            return directory
        return os.path.join(directory, State._get_filename(step_name, run_num, step_num))

    @classmethod
    def _try_convert_from_yaml(cls, name: str, val: Any, param_specs: ParamSpecs, expected_param_type: str) -> Optional[Any]:
        """
        Attempts to convert the object from its yaml form so that it is the correct type.
        :param name: The name of the param being converted.
        :param val: The value of the param to convert.
        :param param_specs: Contains the expected type information.
        :param expected_param_type: The expected type of the param.
        :return: The value if successful converted, else None.
        """
        if ReflectionUtil.is_typed_class(expected_param_type):
            parent_cls, *child_classes = ReflectionUtil.get_typed_class(expected_param_type)
            for cls_ in child_classes:
                if hasattr(cls_, "from_yaml"):
                    try:
                        if parent_cls == "dict":
                            loaded_val = {cls_.from_yaml(item) for item in val.items()}
                        elif parent_cls == "list":
                            loaded_val = [cls_.from_yaml(v) for v in val]
                        else:
                            loaded_val = cls_.from_yaml(val)
                        return cls._check_type(name, loaded_val, param_specs)
                    except Exception as e:
                        continue
                loaded_val = cls._try_convert_from_yaml(name, val, param_specs, cls_)
                if loaded_val is not None:
                    return loaded_val

    @staticmethod
    def _get_filename(step: Any, run_num: int = 1, step_num: int = None) -> str:
        """
        Returns the filename for the given step
        :param step: The name of the step
        :param run_num: The number of times the step has been run
        :param step_num: The number of the step being run
        :return: The filename for the given step
        """
        step = DASH.join(SeparateJoinedWordsStep.separate_camel_case_word(step)).lower()
        if run_num > 1:
            step = f"{step}-{run_num}"
        filename = f"state-{step}"
        if step_num:
            filename = f"{step_num}-{filename}"
        return FileUtil.add_ext(filename, FileUtil.YAML_EXT)

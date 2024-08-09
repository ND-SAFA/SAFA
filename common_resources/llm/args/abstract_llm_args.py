from abc import ABC, abstractmethod
from copy import deepcopy
from dataclasses import dataclass, field
from typing import Any, Dict, List, Type, Union

from common_resources.tools.constants.open_ai_constants import TEMPERATURE_DEFAULT
from common_resources.tools.t_logging.logger_manager import logger
from common_resources.traceability.metrics.supported_trace_metric import SupportedTraceMetric
from common_resources.tools.util.base_object import BaseObject
from common_resources.llm.llm_task import LLMCompletionType


@dataclass
class AbstractLLMArgs(BaseObject, ABC):
    """
    Defines abstract class for arguments of an AI library.
    """
    llm_params: Type
    expected_task_params: Dict[str, List[str]]
    model: str
    temperature: float = TEMPERATURE_DEFAULT
    output_dir: str = None
    metrics: List[str] = field(default_factory=SupportedTraceMetric.get_keys)

    def __post_init__(self) -> None:
        """
        Ensures that all completion types are in the expected task params
        :return: None
        """
        for completion_type in LLMCompletionType:
            if completion_type not in self.expected_task_params:
                self.expected_task_params[completion_type] = []

    def to_params(self, task: str, completion_type: LLMCompletionType, instructions: Dict = None, **kwargs) -> Dict[str, Any]:
        """
        Retrieves the necessary parameters to LLM API using the required parameters defined by task.
        :param task: The task whose required parameters are extracted.
        :param completion_type: Whether the model should complete with generative output or classification
        :param instructions: Commands passed to parameter constructor.
        :param kwargs: Additional instructions to pass to custom parameter construction.
        :return: Mapping of param name to value.
        """
        if instructions is None:
            instructions = {}
        assert task in self.expected_task_params, f"Unknown task {task}." \
                                                  f" Must choose from {self.expected_task_params.keys()}"
        params = {}

        for task_type in [task, completion_type]:
            params = self._add_params_for_task(task_type, params)
            params = self._add_library_params(task_type, params, instructions=instructions)
        params.update(kwargs)

        expected_params = set(vars(self.llm_params).values())
        for param in deepcopy(params):
            if param not in expected_params:
                params.pop(param)
                logger.warning(f"Removing unexpected param for {self.__class__}: {param}")
        return params

    def _add_params_for_task(self, task: Union[str, LLMCompletionType], params: Dict = None) -> Dict:
        """
        Adds the params for a given task
        :param task: The task to add params for
        :param params: The current parameters to add to
        :return: The parameters with task-specific ones added
        """
        if params is None:
            params = {}
        for name in self.expected_task_params[task]:
            val = getattr(self, name)
            if val is None:
                continue
            params[name] = val
        return params

    @classmethod
    def _get_enum_class(cls, child_class_name: str) -> Type:
        """
        Returns the supported enum class for LLM args.
        :param child_class_name: The name of the child to be created.
        :return: The supported enum class.
        """
        from common_resources.llm.args.supported_llm_args import SupportedLLMArgs
        return SupportedLLMArgs

    @abstractmethod
    def _add_library_params(self, task: str, params: Dict, instructions: Dict) -> Dict:
        """
        Adds custom parameters to pass to API for given task.
        :param task: The task being performed with params.
        :param params: The parameters to LLM API.
        :param instructions: Named parameters representing instructions to param construction.
        :return: Dict representing the new parameters.
        """

    @abstractmethod
    def set_max_tokens(self, max_tokens: int) -> None:
        """
        Sets the max tokens parameter for library.
        :param max_tokens: The tokens to set it to.
        :return: None
        """

    @abstractmethod
    def get_max_tokens(self) -> int:
        """
        :return: Returns the max tokens of args.
        """

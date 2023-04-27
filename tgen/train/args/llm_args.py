from abc import ABC, abstractmethod
from typing import Any, Dict, List

from tgen.constants import MAX_TOKENS_DEFAULT
from tgen.data.prompts.prompt_args import PromptArgs
from tgen.train.trainers.trainer_task import TrainerTask


class LLMArgs(ABC):
    """
    Defines abstract class for arguments of an AI library.
    """

    def __init__(self, prompt_args: PromptArgs, expected_task_params: Dict[TrainerTask, List[str]], base_model: str,
                 max_tokens: int = MAX_TOKENS_DEFAULT):
        """
        Constructs AI arguments customized for given prompt arguments and prompt types in creator.
        :param prompt_args: The argument customizing the prompt content.
        :param expected_task_params: Mapping of task names to their expected properties.
        :param max_tokens: The maximum number of allowable tokens to LLM API.
        """
        if max_tokens is None:
            max
        self.prompt_args = prompt_args
        self.expected_task_params = expected_task_params
        self.max_tokens = max_tokens
        self.base_model = base_model

    def to_params(self, task: TrainerTask = TrainerTask.TRAIN, **kwargs) -> Dict[str, Any]:
        """
        Retrieves the necessary parameters to LLM API using the required parameters defined by task.
        :param task: The task whose required parameters are extracted.
        :param kwargs: Additional instructions to pass to custom parameter construction.
        :return: Mapping of param name to value.
        """
        assert task in self.expected_task_params, f"Unknown task {task.value}." \
                                                  f" Must choose from {self.expected_task_params.keys()}"
        params = {}
        if task in [TrainerTask.PREDICT]:  # crete
            self.max_tokens = 1
        params = self._add_params_for_task(TrainerTask.TRAIN if task == TrainerTask.CLASSIFICATION else task, params)
        params = self.add_custom_params(task, params, instructions=kwargs)
        return params

    def _add_params_for_task(self, task: TrainerTask, params: Dict = None) -> Dict:
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

    @abstractmethod
    def add_custom_params(self, task: TrainerTask, params: Dict, instructions: Dict) -> Dict:
        """
        Adds custom parameters to pass to API for given task.
        :param task: The task being performed with params.
        :param params: The parameters to LLM API.
        :param instructions: Named parameters representing instructions to param construction.
        :return: Dict representing the new parameters.
        """

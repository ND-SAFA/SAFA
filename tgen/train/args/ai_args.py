from typing import Any, Dict, List

from tgen.data.prompts.abstract_prompt_creator import AbstractPromptCreator
from tgen.data.prompts.classification_prompt_creator import ClassificationPromptCreator
from tgen.data.prompts.prompt_args import PromptArgs
from tgen.train.trainers.trainer_task import TrainerTask
from tgen.util.ai.params.openai_params import OpenAiParams


class AIArgs:
    """
    Defines abstract class for arguments of an AI library.
    """

    def __init__(self, prompt_args: PromptArgs, prompt_creator: AbstractPromptCreator,
                 expected_params_per_task: Dict[str, List[str]], max_tokens: int):
        """
        Constructs AI arguments customized for given prompt arguments and prompt types in creator.
        :param prompt_args: The argument customizing the prompt content.
        :param prompt_creator: The creator responsible for creating the prompts.
        :param expected_params_per_task: Mapping of task names to their expected properties.
        """
        self.prompt_args = prompt_args
        self.prompt_creator = prompt_creator
        self.expected_task_params = expected_params_per_task
        self.max_tokens = max_tokens

    def to_params(self, task: TrainerTask = TrainerTask.TRAIN, include_classification_metrics: bool = False) -> Dict[str, Any]:
        """
        Gets the params needed for an open ai task
        :param task: The primary task being performed (fine_tune or predict)
        :param include_classification_metrics: If True, includes the params necessary for calculating classification metrics
        :return: A dictionary mapping param name to its value
        """
        assert task in OpenAiParams.EXPECTED_PARAMS_FOR_TASK, f"Unknown task {task.value}." \
                                                              f" Must choose from {OpenAiParams.EXPECTED_PARAMS_FOR_TASK.keys()}"
        params = {}
        if isinstance(self.prompt_creator, ClassificationPromptCreator):
            self.max_tokens = 1
            if include_classification_metrics:
                params = self.__add_params_for_task(TrainerTask.CLASSIFICATION)
                params[OpenAiParams.CLASSIFICATION_POSITIVE_CLASS] = self.prompt_creator.format_completion(
                    self.prompt_creator.pos_class)
        return self.__add_params_for_task(TrainerTask.TRAIN if task == TrainerTask.CLASSIFICATION else task, params)

    def __add_params_for_task(self, task: TrainerTask, params: Dict = None) -> Dict:
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

    def __post_init__(self) -> None:
        """
        Sets specific variables depending on the type of prompt creator
        :return None
        """
        if isinstance(self.prompt_creator, ClassificationPromptCreator):
            self.max_tokens = 1

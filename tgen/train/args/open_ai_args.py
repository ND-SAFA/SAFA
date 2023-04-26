from dataclasses import dataclass, field
from typing import Any, Dict, List

from tgen.constants import COMPUTE_CLASSIFICATION_METRICS_DEFAULT, LEARNING_RATE_MULTIPLIER_DEFAULT, LOGPROBS_DEFAULT, \
    MAX_TOKENS_DEFAULT, \
    TEMPERATURE_DEFAULT
from tgen.data.prompts.abstract_prompt_creator import AbstractPromptCreator
from tgen.data.prompts.classification_prompt_creator import ClassificationPromptCreator
from tgen.train.metrics.supported_trace_metric import SupportedTraceMetric
from tgen.train.trainers.trainer_task import TrainerTask
from tgen.util.ai.open_ai_util import OpenAiUtil


@dataclass
class OpenAiArgs:
    temperature: float = TEMPERATURE_DEFAULT
    max_tokens: int = MAX_TOKENS_DEFAULT
    logprobs: int = LOGPROBS_DEFAULT
    model_suffix: str = None
    n_epochs: int = 1
    learning_rate_multiplier: float = LEARNING_RATE_MULTIPLIER_DEFAULT
    compute_classification_metrics: bool = COMPUTE_CLASSIFICATION_METRICS_DEFAULT
    metrics: List[str] = field(default_factory=SupportedTraceMetric.get_keys)
    output_dir: str = None

    def to_params(self, prompt_creator: AbstractPromptCreator, task: TrainerTask = TrainerTask.TRAIN,
                  include_classification_metrics: bool = False) -> Dict[str, Any]:
        """
        Gets the params needed for an open ai task
        :param prompt_creator: The prompt generator for the trainer
        :param task: The primary task being performed (fine_tune or predict)
        :param include_classification_metrics: If True, includes the params necessary for calculating classification metrics
        :return: A dictionary mapping param name to its value
        """
        assert task in OpenAiUtil.EXPECTED_PARAMS_FOR_TASK, f"Unknown task {task.value}." \
                                                            f" Must choose from {OpenAiUtil.EXPECTED_PARAMS_FOR_TASK.keys()}"
        params = self.__add_params_for_task(TrainerTask.TRAIN if task == TrainerTask.CLASSIFICATION else task)
        if isinstance(prompt_creator, ClassificationPromptCreator):
            if OpenAiUtil.Params.MAX_TOKENS in params:
                params[OpenAiUtil.Params.MAX_TOKENS] = 1
            if include_classification_metrics:
                params = self.__add_params_for_task(TrainerTask.CLASSIFICATION, params)
                params[OpenAiUtil.Params.CLASSIFICATION_POSITIVE_CLASS] = prompt_creator.format_completion(prompt_creator.pos_class)
        return params

    def __add_params_for_task(self, task: TrainerTask, params: Dict = None) -> Dict:
        """
        Adds the params for a given task
        :param task: The task to add params for
        :param params: The current parameters to add to
        :return: The parameters with task-specific ones added
        """
        if params is None:
            params = {}
        for name in OpenAiUtil.EXPECTED_PARAMS_FOR_TASK[task]:
            val = getattr(self, name)
            if val is None:
                continue
            params[name] = val
        return params

from dataclasses import dataclass, field
from typing import Any, Dict, List

from tgen.constants import COMPUTE_CLASSIFICATION_METRICS_DEFAULT, LEARNING_RATE_MULTIPLIER_DEFAULT, LOGPROBS_DEFAULT, \
    MAX_TOKENS_DEFAULT, \
    TEMPERATURE_DEFAULT
from tgen.train.metrics.supported_trace_metric import SupportedTraceMetric
from tgen.train.trainers.trainer_task import TrainerTask
from tgen.data.prompts.abstract_prompt_generator import AbstractPromptGenerator
from tgen.data.prompts.classification_prompt_generator import ClassificationPromptGenerator


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
    __params = {TrainerTask.CLASSIFICATION: ["compute_classification_metrics"],
                TrainerTask.TRAIN: ["model_suffix", "n_epochs", "learning_rate_multiplier"],
                TrainerTask.PREDICT: ["temperature", "max_tokens", "logprobs"]}

    def to_params(self, prompt_generator: AbstractPromptGenerator, task: TrainerTask = TrainerTask.TRAIN) -> Dict[str, Any]:
        """
        Gets the params needed for an open ai task
        :param prompt_generator: The prompt generator for the trainer
        :param task: The primary task being performed (fine_tune or predict)
        :return: A dictionary mapping param name to its value
        """
        assert task in self.__params, f"Unknown task {task.value}. Must choose from {self.__params.keys()}"
        params = self.__add_params_for_task(TrainerTask.TRAIN if task == TrainerTask.CLASSIFICATION else task)
        if isinstance(prompt_generator, ClassificationPromptGenerator) and task == TrainerTask.TRAIN:
            params = self.__add_params_for_task(TrainerTask.CLASSIFICATION, params)
            params["classification_positive_class"] = prompt_generator.format_completion(prompt_generator.pos_class)
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
        for name in self.__params[task]:
            val = getattr(self, name)
            if val is None:
                continue
            params[name] = val
        return params

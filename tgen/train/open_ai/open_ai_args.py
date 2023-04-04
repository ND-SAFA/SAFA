from dataclasses import dataclass, field
from typing import Dict, Any, List

from constants import TEMPERATURE_DEFAULT, MAX_TOKENS_DEFAULT, LOGPROBS_DEFAULT, LEARNING_RATE_MULTIPLIER_DEFAULT, \
    COMPUTE_CLASSIFICATION_METRICS_DEFAULT
from train.metrics.supported_trace_metric import SupportedTraceMetric
from train.open_ai.open_ai_task import OpenAITask


@dataclass
class OpenAIArgs:
    temperature: float = TEMPERATURE_DEFAULT
    max_tokens: int = MAX_TOKENS_DEFAULT
    logprobs: int = LOGPROBS_DEFAULT
    model_suffix: str = None
    n_epochs: int = 1
    learning_rate_multiplier: float = LEARNING_RATE_MULTIPLIER_DEFAULT
    compute_classification_metrics: bool = COMPUTE_CLASSIFICATION_METRICS_DEFAULT
    metrics: List[str] = field(default_factory=SupportedTraceMetric.get_keys)
    __params = {OpenAITask.FINE_TUNE: ["model_suffix", "n_epochs", "learning_rate_multiplier", "compute_classification_metrics"],
                OpenAITask.PREDICT: ["temperature", "max_tokens", "logprobs"]}

    def to_params(self, task: OpenAITask = OpenAITask.FINE_TUNE) -> Dict[str, Any]:
        """
        Gets the params needed for an open ai task
        :param task: The task being performed (fine_tune or predict)
        :return: A dictionary mapping param name to its value
        """
        assert task in self.__params, f"Unknown task {task.value}. Must choose from {self.__params.keys()}"
        params = {}
        for name in self.__params[task]:
            val = getattr(self, name)
            if val is None:
                continue
            params[name] = val
        return params
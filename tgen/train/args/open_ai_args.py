from dataclasses import dataclass, field
from typing import List

from tgen.constants import COMPUTE_CLASSIFICATION_METRICS_DEFAULT, LEARNING_RATE_MULTIPLIER_DEFAULT, LOGPROBS_DEFAULT, \
    MAX_TOKENS_DEFAULT, \
    TEMPERATURE_DEFAULT
from tgen.data.prompts.abstract_prompt_creator import AbstractPromptCreator
from tgen.data.prompts.classification_prompt_creator import ClassificationPromptCreator
from tgen.data.prompts.prompt_args import PromptArgs
from tgen.train.args.ai_args import AIArgs
from tgen.train.metrics.supported_trace_metric import SupportedTraceMetric
from tgen.train.trainers.trainer_task import TrainerTask


class OpenAIParams:
    """
    Contains possible parameters to OpenAI API.
    """
    COMPUTE_CLASSIFICATION_METRICS = "compute_classification_metrics"
    MODEL_SUFFIX = "model_suffix"
    N_EPOCHS = "n_epochs"
    LEARNING_RATE_MULTIPLIER = "learning_rate_multiplier"
    TEMPERATURE = "temperature"
    MAX_TOKENS = "max_tokens"
    LOG_PROBS = "logprobs"
    PROMPT = "prompt"
    VALIDATION_FILE = "validation_file"
    CLASSIFICATION_POSITIVE_CLASS = "classification_positive_class"


@dataclass
class OpenAiArgs(AIArgs):
    temperature: float = TEMPERATURE_DEFAULT
    max_tokens: int = MAX_TOKENS_DEFAULT
    logprobs: int = LOGPROBS_DEFAULT
    model_suffix: str = None
    n_epochs: int = 1
    learning_rate_multiplier: float = LEARNING_RATE_MULTIPLIER_DEFAULT
    compute_classification_metrics: bool = COMPUTE_CLASSIFICATION_METRICS_DEFAULT
    metrics: List[str] = field(default_factory=SupportedTraceMetric.get_keys)
    prompt_args = PromptArgs(prompt_separator="\n\n###\n\n", completion_prefix=" ", completion_suffix="###")
    prompt_creator: AbstractPromptCreator = ClassificationPromptCreator(prompt_args=prompt_args)
    output_dir: str = None
    expected_task_params = {TrainerTask.CLASSIFICATION: [OpenAIParams.COMPUTE_CLASSIFICATION_METRICS],
                            TrainerTask.TRAIN: [OpenAIParams.MODEL_SUFFIX, OpenAIParams.N_EPOCHS,
                                                OpenAIParams.LEARNING_RATE_MULTIPLIER],
                            TrainerTask.PREDICT: [OpenAIParams.TEMPERATURE, OpenAIParams.MAX_TOKENS, OpenAIParams.LOG_PROBS]}

from dataclasses import dataclass, field
from typing import Dict, List

from tgen.constants.open_ai_constants import COMPUTE_CLASSIFICATION_METRICS_DEFAULT, LEARNING_RATE_MULTIPLIER_DEFAULT, LOGPROBS_DEFAULT, \
    MAX_TOKENS_DEFAULT, \
    TEMPERATURE_DEFAULT
from tgen.data.prompts.prompt_args import PromptArgs
from tgen.train.args.llm_args import LLMArgs
from tgen.train.metrics.supported_trace_metric import SupportedTraceMetric
from tgen.train.trainers.trainer_task import TrainerTask
from tgen.util.ai.params.openai_params import OpenAiParams


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
class OpenAiArgs(LLMArgs):
    temperature: float = TEMPERATURE_DEFAULT
    max_tokens: int = MAX_TOKENS_DEFAULT
    logprobs: int = LOGPROBS_DEFAULT
    model_suffix: str = None
    n_epochs: int = 1
    learning_rate_multiplier: float = LEARNING_RATE_MULTIPLIER_DEFAULT
    compute_classification_metrics: bool = COMPUTE_CLASSIFICATION_METRICS_DEFAULT
    metrics: List[str] = field(default_factory=SupportedTraceMetric.get_keys)
    prompt_args = PromptArgs(prompt_separator="\n\n###\n\n", completion_prefix=" ", completion_suffix="###")
    output_dir: str = None
    expected_task_params = {TrainerTask.CLASSIFICATION: [OpenAIParams.COMPUTE_CLASSIFICATION_METRICS],
                            TrainerTask.TRAIN: [OpenAIParams.MODEL_SUFFIX, OpenAIParams.N_EPOCHS,
                                                OpenAIParams.LEARNING_RATE_MULTIPLIER],
                            TrainerTask.PREDICT: [OpenAIParams.TEMPERATURE, OpenAIParams.MAX_TOKENS, OpenAIParams.LOG_PROBS]}
    base_model = CLASSIFICATION_MODEL_DEFAULT

    def add_custom_params(self, task: TrainerTask, params: Dict, instructions: Dict) -> Dict:
        """
        Allows the usage of custom params defined in instructions. Includes classification metrics.
        :param task: The task being performed.
        :param params: The parameters current being constructed.
        :param instructions: Any custom instruction flags.
        :return: Parameters with customizations added.
        """
        if instructions.get("include_classification_metrics", None):
            assert "prompt_creator" in instructions, "Expected prompt_creator to be defined when including classification metrics."
            prompt_creator = instructions["prompt_creator"]
            assert hasattr(prompt_creator, "pos_class"), "Expected prompt creator to define `pos_class`"
            pos_class = getattr(prompt_creator, "pos_class")
            params = self._add_params_for_task(TrainerTask.CLASSIFICATION)
            params[OpenAiParams.CLASSIFICATION_POSITIVE_CLASS] = prompt_creator.format_completion(pos_class)
        return params

from dataclasses import dataclass
from typing import Dict

from tgen.constants.open_ai_constants import CLASSIFICATION_MODEL_DEFAULT, COMPUTE_CLASSIFICATION_METRICS_DEFAULT, \
    LEARNING_RATE_MULTIPLIER_DEFAULT, LOGPROBS_DEFAULT
from tgen.data.prompts.prompt_args import PromptArgs
from tgen.models.llm.llm_task import LLMCompletionType
from tgen.train.args.abstract_llm_args import AbstractLLMArgs
from tgen.train.trainers.trainer_task import TrainerTask
from tgen.util.override import overrides


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
class OpenAIArgs(AbstractLLMArgs):
    TASK_PARAMS = {LLMCompletionType.CLASSIFICATION: [OpenAIParams.COMPUTE_CLASSIFICATION_METRICS],
                   TrainerTask.TRAIN: [OpenAIParams.MODEL_SUFFIX, OpenAIParams.N_EPOCHS,
                                       OpenAIParams.LEARNING_RATE_MULTIPLIER],
                   TrainerTask.PREDICT: [OpenAIParams.TEMPERATURE, OpenAIParams.MAX_TOKENS, OpenAIParams.LOG_PROBS]}

    def __init__(self, model: str = CLASSIFICATION_MODEL_DEFAULT, logprobs: int = LOGPROBS_DEFAULT,
                 n_epochs: int = 1, learning_rate_multiplier: float = LEARNING_RATE_MULTIPLIER_DEFAULT,
                 compute_classification_metrics: bool = COMPUTE_CLASSIFICATION_METRICS_DEFAULT, model_suffix: str = None,
                 **kwargs):
        """
        Constructs OpenAI args with given model
        :param model:
        :param kwargs:
        """
        self.logprobs = logprobs
        self.n_epochs = n_epochs
        self.learning_rate_multiplier = learning_rate_multiplier,
        self.compute_classification_metrics = compute_classification_metrics
        self.model_suffix = model_suffix
        super().__init__(model=model, expected_task_params=self.TASK_PARAMS, **kwargs)

    @overrides(AbstractLLMArgs)
    def _add_library_params(self, task: TrainerTask, params: Dict, instructions: Dict) -> Dict:
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
            params = self._add_params_for_task(LLMCompletionType.CLASSIFICATION)
            params[OpenAIParams.CLASSIFICATION_POSITIVE_CLASS] = prompt_creator.format_completion(pos_class)
        return params

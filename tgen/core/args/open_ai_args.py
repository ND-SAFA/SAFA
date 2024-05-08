from dataclasses import dataclass
from typing import Dict

from tgen.common.constants.open_ai_constants import COMPUTE_CLASSIFICATION_METRICS_DEFAULT, LEARNING_RATE_MULTIPLIER_DEFAULT, \
    LOGPROBS_DEFAULT, MAX_TOKENS_DEFAULT, OPEN_AI_MODEL_DEFAULT
from tgen.common.util.dataclass_util import DataclassUtil
from tgen.common.util.dict_util import DictUtil
from tgen.common.util.override import overrides
from tgen.core.args.abstract_llm_args import AbstractLLMArgs
from tgen.core.trainers.trainer_task import TrainerTask
from tgen.prompts.llm_prompt_build_args import LLMPromptBuildArgs


class OpenAIParams:
    """
    Contains possible parameters to OpenAI API.
    """
    MODEL = "model"
    COMPUTE_CLASSIFICATION_METRICS = "compute_classification_metrics"
    MODEL_SUFFIX = "model_suffix"
    N_EPOCHS = "n_epochs"
    LEARNING_RATE_MULTIPLIER = "learning_rate_multiplier"
    TEMPERATURE = "temperature"
    MAX_TOKENS = "max_tokens"
    LOG_PROBS = "logprobs"
    PROMPT = "prompt"
    MESSAGES = "messages"
    VALIDATION_FILE = "validation_file"
    CLASSIFICATION_POSITIVE_CLASS = "classification_positive_class"


@dataclass
class OpenAIArgs(AbstractLLMArgs):
    logprobs: int = LOGPROBS_DEFAULT
    n_epochs: int = 1
    learning_rate_multiplier: float = LEARNING_RATE_MULTIPLIER_DEFAULT
    compute_classification_metrics: bool = COMPUTE_CLASSIFICATION_METRICS_DEFAULT
    model_suffix: str = None
    max_tokens: int = MAX_TOKENS_DEFAULT
    prompt_args: LLMPromptBuildArgs = None
    _EXPECTED_TASK_PARAMS = {TrainerTask.TRAIN: [OpenAIParams.MODEL, OpenAIParams.MODEL_SUFFIX, OpenAIParams.N_EPOCHS,
                                                 OpenAIParams.LEARNING_RATE_MULTIPLIER],
                             TrainerTask.PREDICT: [OpenAIParams.MODEL, OpenAIParams.TEMPERATURE, OpenAIParams.MAX_TOKENS,
                                                   OpenAIParams.LOG_PROBS]}

    def __init__(self, **kwargs):
        """
        Sets all necessary args for OpenAI
        :param kwargs: Contains all necessary arg name to value mappings
        """
        super_args = DataclassUtil.set_unique_args(self, AbstractLLMArgs, **kwargs)
        DictUtil.update_kwarg_values(super_args, replace_existing=False, model=OPEN_AI_MODEL_DEFAULT)
        super().__init__(expected_task_params=self._EXPECTED_TASK_PARAMS, llm_params=OpenAIParams, **super_args)

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
            assert "prompt_builder" in instructions, "Expected prompt_creator to be defined when including classification metrics."
            prompt_creator = instructions["prompt_builder"]
            pos_class = None
            for prompt in prompt_creator.prompts:
                choices = getattr(prompt, "choices", None)
                if choices is not None:
                    pos_class = choices[0]
                    break
            assert pos_class is not None, "Expected prompt creator to define `pos_class`"
            params[OpenAIParams.CLASSIFICATION_POSITIVE_CLASS] = prompt_creator._format_completion(pos_class, self.prompt_args, )
            params[OpenAIParams.COMPUTE_CLASSIFICATION_METRICS] = True
        return params

    def set_max_tokens(self, max_tokens: int) -> None:
        """
        Sets the number of max tokens for the LLM library.
        :param max_tokens: The new max tokens to set it too.
        :return: None
        """
        self.max_tokens = max_tokens

    def get_max_tokens(self) -> int:
        """
        :return: Returns the current max tokens.
        """
        return self.max_tokens

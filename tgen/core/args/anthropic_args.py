from typing import Dict

from tgen.common.constants.anthropic_constants import ANTHROPIC_MODEL_DEFAULT
from tgen.common.constants.open_ai_constants import MAX_TOKENS_DEFAULT
from tgen.common.util.dataclass_util import DataclassUtil
from tgen.common.util.dict_util import DictUtil
from tgen.core.args.abstract_llm_args import AbstractLLMArgs
from tgen.core.trainers.trainer_task import TrainerTask


class AnthropicParams:
    """
    Contains allowed parameters to anthropic API.
    """
    PROMPT = "prompt"
    SYSTEM = "system"
    MESSAGES = "messages"
    MODEL = "model"  # claude-v1, claude-v1.2, claude-v1.3, claude-instant-v1, claude-instant-v1.0
    MAX_TOKENS = "max_tokens"
    STOP_SEQUENCES = "stop_sequences"  # List of strings that will stop prediction when encountered.
    STREAM = "stream"  # NOT SUPPORTED.
    TEMPERATURE = "temperature"
    TOP_K = "top_k"
    top_p = "top_p"  # Nucleus sampling selects top probability tokens, alter temperature or top_p.


class AnthropicArgs(AbstractLLMArgs):
    """
    Defines allowable arguments to anthropic API.
    """

    max_tokens: int = MAX_TOKENS_DEFAULT
    _EXPECTED_TASK_PARAMS = {TrainerTask.TRAIN: [],
                             TrainerTask.PREDICT: [AnthropicParams.MODEL, AnthropicParams.TEMPERATURE,
                                                   AnthropicParams.MAX_TOKENS]}

    def __init__(self, **kwargs):
        """
        Sets all necessary args for Anthropic
        :param kwargs: Contains all necessary arg name to value mappings
        """
        super_args = DataclassUtil.set_unique_args(self, AbstractLLMArgs, **kwargs)
        DictUtil.update_kwarg_values(super_args, replace_existing=False, model=ANTHROPIC_MODEL_DEFAULT)
        super().__init__(expected_task_params=self._EXPECTED_TASK_PARAMS, llm_params=AnthropicParams, **super_args)

    def _add_library_params(self, task: TrainerTask, params: Dict, instructions: Dict) -> Dict:
        """
        Allows the usage of custom params defined in instructions. Currently unused for Anthropic
        :param task: The task being performed.
        :param params: The parameters current being constructed.
        :param instructions: Any custom instruction flags.
        :return: Parameters with customizations added.
        """
        return params

    def set_max_tokens(self, max_tokens: int) -> None:
        """
        Sets the max tokens of anthropic params.
        :param max_tokens: The max tokens to set it to.
        :return: None
        """
        self.max_tokens = max_tokens

    def get_max_tokens(self) -> int:
        """
        :return: Returns the max tokens of args.
        """
        return self.max_tokens

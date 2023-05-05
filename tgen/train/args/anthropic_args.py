from tgen.constants.anthropic_constants import ANTHROPIC_MODEL_DEFAULT
from tgen.constants.open_ai_constants import MAX_TOKENS_DEFAULT
from tgen.data.prompts.prompt_args import PromptArgs
from tgen.models.llm.llm_task import LLMCompletionType
from tgen.train.args.abstract_llm_args import AbstractLLMArgs
from tgen.train.trainers.trainer_task import TrainerTask


class AnthropicParams:
    """
    Contains allowed parameters to anthropic API.
    """
    PROMPT = "prompt"
    MODEL = "model"  # claude-v1, claude-v1.2, claude-v1.3, claude-instant-v1, claude-instant-v1.0
    MAX_TOKENS_TO_SAMPLE = "max_tokens_to_sample"
    STOP_SEQUENCES = "stop_sequences"  # List of strings that will stop prediction when encountered.
    STREAM = "stream"  # NOT SUPPORTED.
    TEMPERATURE = "temperature"
    TOP_K = "top_k"
    top_p = "top_p"  # Nucleus sampling selects top probability tokens, alter temperature or top_p.


class AnthropicArgs(AbstractLLMArgs):
    """
    Defines allowable arguments to anthropic API.
    """

    max_tokens_to_sample = MAX_TOKENS_DEFAULT
    prompt_args = PromptArgs(prompt_prefix="\n\nHuman:", prompt_suffix="\n\nAssistant:", completion_prefix=" ",
                             completion_suffix="###")

    def __init__(self, model: str = ANTHROPIC_MODEL_DEFAULT, **kwargs):
        self.prompt_args = self.prompt_args
        self.expected_task_params = {LLMCompletionType.CLASSIFICATION: [AnthropicParams.MAX_TOKENS_TO_SAMPLE],
                                     TrainerTask.TRAIN: [AnthropicParams.MODEL],
                                     TrainerTask.PREDICT: [AnthropicParams.TEMPERATURE, AnthropicParams.MAX_TOKENS_TO_SAMPLE]}
        super().__init__(self.expected_task_params, model, **kwargs)

    def set_max_tokens(self, max_tokens: int) -> None:
        """
        Sets the max tokens of anthropic params.
        :param max_tokens: The max tokens to set it to.
        :return: None
        """
        self.max_tokens_to_sample = max_tokens

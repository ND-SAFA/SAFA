from typing import Dict, List

from tgen.data.prompts.prompt_args import PromptArgs
from tgen.train.args.llm_args import LLMArgs
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


class AnthropicArgs(LLMArgs):
    """
    Defines allowable arguments to anthropic API.
    """

    def __init__(self, expected_task_params: Dict[TrainerTask, List[str]], base_model: str):
        self.prompt_args = PromptArgs(prompt_separator="\n\nAssistant:", completion_prefix=" ", completion_suffix="###")
        self.expected_task_params = {TrainerTask.CLASSIFICATION: [],
                                     TrainerTask.TRAIN: [AnthropicParams.MODEL],
                                     TrainerTask.PREDICT: [AnthropicParams.TEMPERATURE, AnthropicParams.MAX_TOKENS_TO_SAMPLE]}
        super().__init__(self.prompt_args, expected_task_params, base_model)

    def add_custom_params(self, task: TrainerTask, params: Dict, instructions: Dict) -> Dict:
        """
        Adds any custom parameters.
        :param task: The task being performed.
        :param params: The base parameters
        :param instructions: Any additional instructions passed to param construction.
        :return: Params with customizations.
        """
        if "max_tokens" in params:
            max_tokens = params.pop("max_tokens")
            params[AnthropicParams.MAX_TOKENS_TO_SAMPLE] = max_tokens
        return params

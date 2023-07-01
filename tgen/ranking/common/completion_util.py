from typing import List

from tgen.models.llm.anthropic_manager import AnthropicManager
from tgen.models.llm.llm_task import LLMCompletionType


def complete_prompts(prompts: List[str], max_tokens: int = 400, temperature: float = 0, **kwargs):
    """
    Utility method for completing prompts via Anthropics large context models.
    :param prompts: The prompts to fulfill.
    :param max_tokens: The max tokens to generate per prompt.
    :param temperature: The temperature of the model
    :param kwargs: Keyword arguments.
    :return: Responses.
    """
    manager = AnthropicManager()
    params = {
        "prompt": [f"\n\nHuman: {p}\n\nAssistant:" for p in prompts],
        "max_tokens_to_sample": max_tokens,
        "temperature": temperature,
        **kwargs
    }
    batch_response = manager.make_completion_request(LLMCompletionType.GENERATION, **params)
    return batch_response

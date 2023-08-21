from typing import List

from tgen.data.prompts.prompt import Prompt
from tgen.data.prompts.prompt_builder import PromptBuilder
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
    built_prompts = []
    for p in prompts:
        prompt_builder = PromptBuilder(prompts=[Prompt(p)])
        built_p = prompt_builder.build(manager.prompt_args)
        built_prompts.append(built_p)
    params = {
        "prompt": built_prompts,
        **kwargs,
    }
    manager.llm_args.set_max_tokens(max_tokens)
    manager.llm_args.temperature = temperature
    batch_response = manager.make_completion_request(LLMCompletionType.GENERATION, **params)
    return batch_response

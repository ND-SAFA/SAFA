import os.path

from api.endpoints.completion.completion_serializer import CompletionPayload, CompletionSerializer
from api.endpoints.endpoint import endpoint
from api.utils.model_util import ModelUtil
from tgen.common.util.reflection_util import ReflectionUtil
from tgen.models.llm.abstract_llm_manager import AbstractLLMManager
from tgen.models.llm.anthropic_manager import AnthropicManager
from tgen.models.llm.open_ai_manager import OpenAIManager

JOB_DIR = os.path.expanduser("~/.cache/safa/jobs")


def complete_prompt(model: str, prompt: str, llm_manager: AbstractLLMManager, **params) -> str:
    """
    Performs a completion for a prompt.
    :param model: The model to use.
    :param prompt: The prompt to complete.
    :param llm_manager: The LLM utility file giving access to API.
    :param params: Additional parameters to API call.
    :return:
    """
    if ReflectionUtil.is_instance_or_subclass(llm_manager, OpenAIManager):
        prompt_args = OpenAIManager.prompt_args
    elif ReflectionUtil.is_instance_or_subclass(llm_manager, AnthropicManager):
        prompt_args = AnthropicManager.prompt_args
    else:
        raise Exception("Unknown LLM library:" + llm_manager.__class__.__name__)
    raise NotImplemented("Completion endpoint is under construction!")


@endpoint(CompletionSerializer)
def perform_completion(prediction_payload: CompletionPayload):
    """
    Endpoint for performing completion of prompt.
    :param prediction_payload: The completion request.
    :return: Completion response.
    """
    llm_name = "anthropic"
    prompt: str = prediction_payload["prompt"]
    model, llm_manager = ModelUtil.get_model_manager(llm_name)
    completion = complete_prompt(model, prompt, llm_manager)
    return {"completion": completion}

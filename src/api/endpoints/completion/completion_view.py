import os.path

from celery import shared_task

from api.endpoints.base.views.endpoint import endpoint
from api.endpoints.completion.completion_serializer import CompletionPayload, CompletionSerializer
from api.utils.model_util import ModelUtil
from tgen.data.prompts.generation_prompt_creator import GenerationPromptCreator
from tgen.models.llm.abstract_llm_manager import AbstractLLMManager
from tgen.models.llm.anthropic_manager import AnthropicManager
from tgen.models.llm.llm_responses import SupportedLLMResponses
from tgen.models.llm.llm_task import LLMCompletionType
from tgen.models.llm.open_ai_manager import OpenAIManager
from tgen.util.reflection_util import ReflectionUtil

JOB_DIR = os.path.expanduser("~/.cache/safa/jobs")


def perform_completion(model: str, prompt: str, llm_manager: AbstractLLMManager, **params) -> str:
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
    prompt_creator = GenerationPromptCreator(prompt_args=prompt_args)
    formatted_prompt = prompt_creator.format_prompt(prompt)

    llm_response: SupportedLLMResponses = llm_manager.make_completion_request(completion_type=LLMCompletionType.GENERATION,
                                                                              prompt=[formatted_prompt],
                                                                              model=model,
                                                                              **params)
    model_response = llm_response.batch_responses[0]
    return model_response


@endpoint(CompletionSerializer)
@shared_task
def perform_completion(prediction_payload: CompletionPayload):
    """
    Endpoint for performing completion of prompt.
    :param prediction_payload: The completion request.
    :return: Completion response.
    """
    llm_name = prediction_payload["model"].lower()
    prompt: str = prediction_payload["prompt"]
    model, llm_manager = ModelUtil.get_model_manager(llm_name)
    completion = perform_completion(model, prompt, llm_manager)
    return {"completion": completion}

import os.path

from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView

from api.endpoints.generation.generation_serializer import GenerationSerializer
from api.utils.view_util import ViewUtil
from tgen.data.prompts.generation_prompt_creator import GenerationPromptCreator
from tgen.train.args.anthropic_args import AnthropicArgs
from tgen.train.args.open_ai_args import OpenAIArgs
from tgen.train.trainers.trainer_task import TrainerTask
from tgen.util.json_util import NpEncoder
from tgen.util.llm.anthropic_util import AnthropicUtil
from tgen.util.llm.llm_responses import GenerationResponse
from tgen.util.llm.llm_task import LLMTask
from tgen.util.llm.llm_util import LLMUtil
from tgen.util.llm.open_ai_util import OpenAIUtil
from tgen.util.llm.supported_ai_utils import SupportedLLMUtils
from tgen.util.reflection_util import ReflectionUtil

JOB_DIR = os.path.expanduser("~/.cache/safa/jobs")


class GenerationView(APIView):
    """
    Provides endpoints for accessing completion API of LLM libraries.
    """

    @csrf_exempt
    def post(self, request: HttpRequest):
        prediction_payload = ViewUtil.read_request(request, GenerationSerializer)
        llm_name = prediction_payload["model"].lower()
        prompt: str = prediction_payload["prompt"]

        model_map = {
            "gpt": {
                "model": "text-davinci-003",
                "util": SupportedLLMUtils.OPENAI.value
            },
            "anthropic": {
                "model": "claude-v1.3",
                "util": SupportedLLMUtils.ANTHROPIC.value
            }
        }
        assert llm_name in model_map, f"Model should be one of {list(model_map.keys())}"
        model = model_map[llm_name]["model"]
        llm_util = model_map[llm_name]["util"]
        completion = self.perform_completion(model, prompt, llm_util)
        return JsonResponse({"completion": completion}, encoder=NpEncoder)

    @staticmethod
    def perform_completion(model: str, prompt: str, llm_util: LLMUtil, **params) -> str:
        """
        Performs a completion for a prompt.
        :param model: The model to use.
        :param prompt: The prompt to complete.
        :param llm_util: The LLM utility file giving access to API.
        :param param: Additional parameters to API call.
        :return:
        """
        if ReflectionUtil.is_instance_or_subclass(llm_util, OpenAIUtil):
            prompt_args = OpenAIArgs.prompt_args
            trainer_args = OpenAIArgs()
        elif ReflectionUtil.is_instance_or_subclass(llm_util, AnthropicUtil):
            prompt_args = AnthropicArgs.prompt_args
            trainer_args = AnthropicArgs()
        else:
            raise Exception("Unknown LLM library:" + llm_util.__class__.__name__)
        prompt_creator = GenerationPromptCreator(prompt_args=prompt_args)
        formatted_prompt = prompt_creator.format_prompt(prompt)
        params = trainer_args.to_params(TrainerTask.PREDICT, include_classification_metrics=False,
                                        prompt_creator=prompt_creator)
        llm_response: GenerationResponse = llm_util.make_completion_request(task=LLMTask.GENERATION,
                                                                            prompt=[formatted_prompt],
                                                                            model=model,
                                                                            **params)
        model_response = llm_response.batch_responses[0]
        return model_response

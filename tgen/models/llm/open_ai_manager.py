from collections import namedtuple

import openai
from openai.openai_object import OpenAIObject

from tgen.common.constants import open_ai_constants
from tgen.common.constants.environment_constants import IS_TEST, OPEN_AI_KEY, OPEN_AI_ORG
from tgen.common.util.logging.logger_manager import logger
from tgen.common.util.thread_util import ThreadUtil
from tgen.core.args.open_ai_args import OpenAIArgs, OpenAIParams
from tgen.models.llm.abstract_llm_manager import AIObject, AbstractLLMManager
from tgen.models.llm.llm_responses import ClassificationItemResponse, ClassificationResponse, GenerationResponse, SupportedLLMResponses
from tgen.models.llm.llm_task import LLMCompletionType
from tgen.prompts.prompt_args import PromptArgs

if not IS_TEST:
    assert OPEN_AI_ORG and OPEN_AI_KEY, f"Must supply value for {f'{OPEN_AI_ORG=}'.split('=')[0]} " \
                                        f"and {f'{OPEN_AI_KEY=}'.split('=')[0]} in .env"
    openai.organization = OPEN_AI_ORG
    openai.api_key = OPEN_AI_KEY

Res = namedtuple('Res', ['choices'])


class OpenAIManager(AbstractLLMManager[OpenAIObject]):
    prompt_args = PromptArgs(prompt_prefix="", prompt_suffix="\n>", completion_prefix="", completion_suffix="")

    def __init__(self, llm_args: OpenAIArgs = None):
        """
        Initializes with args used for the requests to Anthropic model
        :param llm_args: args used for the requests to Anthropic model
        """
        if llm_args is None:
            llm_args = OpenAIArgs(prompt_args=self.prompt_args)
        assert isinstance(llm_args, OpenAIArgs), "Must use OpenAI args with OpenAI manager"
        llm_args.prompt_args = self.prompt_args
        super().__init__(llm_args=llm_args, prompt_args=self.prompt_args)
        logger.info(f"Created OpenAI manager with Model: {self.llm_args.model}")

    def _make_fine_tune_request_impl(self, **kwargs) -> OpenAIObject:
        """
        Makes a request to fine-tune a model
        :param kwargs: Params necessary for request
        :return: The response from open  ai
        """
        result = openai.FineTune.create(**kwargs)
        if result is None:  # retry if failed.
            result = openai.FineTune.create(**kwargs)
        return result

    def retrieve_fine_tune_request(self, **params) -> OpenAIObject:
        """
        Retrieves s a request to fine-tune a model
        :return: The response from open  ai
        """
        return openai.FineTune.retrieve(**params)

    def make_completion_request_impl(self, **params) -> AIObject:
        """
        Makes a request to completion a model
        :param params: Params necessary for request
        :return: The response from open  ai
        """
        params.pop(OpenAIParams.LOG_PROBS)
        prompt = params.pop(OpenAIParams.PROMPT)
        prompts = prompt if isinstance(prompt, list) else [prompt]
        logger.info(f"Starting OpenAI batch: {params['model']}")

        def complete_prompt(p: str) -> str:
            """
            Completes the prompt with openai manager.
            :param p: The prompt to complete.
            :return: The response as a string.
            """
            params[OpenAIParams.MESSAGES] = [{"role": "user", "content": p}]
            res = openai.ChatCompletion.create(**params)
            return res.choices[0]

        choices = ThreadUtil.multi_thread_process("Making completion requests",
                                                  prompts,
                                                  complete_prompt,
                                                  n_threads=open_ai_constants.OPENAI_MAX_THREADS,
                                                  max_attempts=open_ai_constants.OPENAI_MAX_ATTEMPTS,
                                                  collect_results=True)

        return Res(choices=choices)

    @staticmethod
    def translate_to_response(task: LLMCompletionType, res: OpenAIObject, **params) -> SupportedLLMResponses:
        """
        Translates the response to the response for task.
        :param task: The task to translate to.
        :param res: OpenAI response.
        :param params: The parameters to the API.
        :return: A response for the supported types.
        """
        text_responses = [choice.message["content"].strip() for choice in res.choices]
        if task == LLMCompletionType.GENERATION:
            return GenerationResponse(text_responses)
        elif task == LLMCompletionType.CLASSIFICATION:
            probs = [r.logprobs.top_logprobs[0] for r in res.choices]
            classification_items = [ClassificationItemResponse(t, probs=p) for t, p in zip(text_responses, probs)]
            return ClassificationResponse(classification_items)
        else:
            raise NotImplementedError(f"No handler for {task.name} is implemented")

    def upload_file(self, **params) -> OpenAIObject:
        """
        Makes a request to upload a file
        :param params: Params necessary for request
        :return: The response from open  ai
        """
        return openai.File.create(**params)

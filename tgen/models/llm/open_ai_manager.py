import openai
from openai.openai_object import OpenAIObject

from tgen.constants.environment_constants import IS_TEST, OPEN_AI_KEY, OPEN_AI_ORG
from tgen.data.prompts.prompt_args import PromptArgs
from tgen.models.llm.abstract_llm_manager import AIObject, AbstractLLMManager
from tgen.models.llm.llm_responses import ClassificationItemResponse, ClassificationResponse, GenerationResponse, SupportedLLMResponses
from tgen.models.llm.llm_task import LLMCompletionType
from tgen.train.args.open_ai_args import OpenAIArgs, OpenAIParams
from tgen.util.list_util import ListUtil
from tgen.util.logging.logger_manager import logger
from tgen.util.logging.tgen_tqdm import tgen_tqdm

if not IS_TEST:
    assert OPEN_AI_ORG and OPEN_AI_KEY, f"Must supply value for {f'{OPEN_AI_ORG=}'.split('=')[0]} " \
                                        f"and {f'{OPEN_AI_KEY=}'.split('=')[0]} in .env"
    openai.organization = OPEN_AI_ORG
    openai.api_key = OPEN_AI_KEY


class OpenAIManager(AbstractLLMManager[OpenAIObject]):
    MAX_COMPLETION_PROMPTS: int = 20
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
        assert not IS_TEST, "No requests should be made while in test"
        prompt = params.get(OpenAIParams.PROMPT)
        batches = ListUtil.batch(prompt, n=OpenAIManager.MAX_COMPLETION_PROMPTS) if isinstance(prompt, list) else [prompt]
        res = None
        logger.info(f"Starting OpenAI batch: {params['model']}")
        for batch in tgen_tqdm(batches, desc="Making completion requests"):
            params[OpenAIParams.PROMPT] = batch
            batch_res = openai.Completion.create(**params)
            if res is None:
                res = batch_res
            else:
                res.choices.extend(batch_res.choices)
        return res

    @staticmethod
    def translate_to_response(task: LLMCompletionType, res: OpenAIObject, **params) -> SupportedLLMResponses:
        """
        Translates the response to the response for task.
        :param task: The task to translate to.
        :param res: OpenAI response.
        :param params: The parameters to the API.
        :return: A response for the supported types.
        """
        text_responses = [choice.text.strip() for choice in res.choices]
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

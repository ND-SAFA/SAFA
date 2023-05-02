import time

import openai
from openai.openai_object import OpenAIObject
from tqdm import tqdm

from tgen.constants.environment_constants import IS_TEST, OPEN_AI_KEY, OPEN_AI_ORG
from tgen.train.args.open_ai_args import OpenAIParams
from tgen.util.list_util import ListUtil
from tgen.util.llm.llm_util import LLMUtil

if not IS_TEST:
    assert OPEN_AI_ORG and OPEN_AI_KEY, f"Must supply value for {f'{OPEN_AI_ORG=}'.split('=')[0]} " \
                                        f"and {f'{OPEN_AI_KEY=}'.split('=')[0]} in .env"
    openai.organization = OPEN_AI_ORG
    openai.api_key = OPEN_AI_KEY


class OpenAIUtil(LLMUtil[OpenAIObject]):
    MAX_COMPLETION_PROMPTS: int = 20

    @staticmethod
    def make_fine_tune_request(**params) -> OpenAIObject:
        """
        Makes a request to fine-tune a model
        :param params: Params necessary for request
        :return: The response from open  ai
        """
        return openai.FineTune.create(**params)

    @staticmethod
    def retrieve_fine_tune_request(**params) -> OpenAIObject:
        """
        Retrieves s a request to fine-tune a model
        :param params: Params necessary for request
        :return: The response from open  ai
        """
        return openai.FineTune.retrieve(**params)

    @staticmethod
    def make_completion_request(**params) -> OpenAIObject:
        """
        Makes a request to completion a model
        :param params: Params necessary for request
        :return: The response from open  ai
        """
        prompt = params.get(OpenAIParams.PROMPT)
        batches = ListUtil.batch(prompt, n=OpenAIUtil.MAX_COMPLETION_PROMPTS) if isinstance(prompt, list) else [prompt]
        res = None
        for batch in tqdm(batches, desc="Making completion requests"):
            params[OpenAIParams.PROMPT] = batch
            batch_res = openai.Completion.create(**params)
            if res is None:
                res = batch_res
            else:
                res.choices.extend(batch_res.choices)
            time.sleep(.1)  # trying to avoid rate limit
        return res

    @staticmethod
    def upload_file(**params) -> OpenAIObject:
        """
        Makes a request to upload a file
        :param params: Params necessary for request
        :return: The response from open  ai
        """
        return openai.File.create(**params)

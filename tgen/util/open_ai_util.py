import openai
from openai.openai_object import OpenAIObject

from tgen.constants.environment_constants import IS_TEST
from tgen.constants.environment_constants import OPEN_AI_ORG, OPEN_AI_KEY
from tgen.train.trainers.trainer_task import TrainerTask
from tgen.util.list_util import ListUtil

if not IS_TEST:
    assert OPEN_AI_ORG and OPEN_AI_KEY, f"Must supply value for {f'{OPEN_AI_ORG=}'.split('=')[0]} " \
                                        f"and {f'{OPEN_AI_KEY=}'.split('=')[0]} in .env"
    openai.organization = OPEN_AI_ORG
    openai.api_key = OPEN_AI_KEY


class OpenAiUtil:

    class Params:
        COMPUTE_CLASSIFICATION_METRICS = "compute_classification_metrics"
        MODEL_SUFFIX = "model_suffix"
        N_EPOCHS = "n_epochs"
        LEARNING_RATE_MULTIPLIER = "learning_rate_multiplier"
        TEMPERATURE = "temperature"
        MAX_TOKENS = "max_tokens"
        LOG_PROBS = "logprobs"
        PROMPT = "prompt"
        VALIDATION_FILE = "validation_file"
        CLASSIFICATION_POSITIVE_CLASS = "classification_positive_class"

    MAX_COMPLETION_PROMPTS: int = 20
    EXPECTED_PARAMS_FOR_TASK = {TrainerTask.CLASSIFICATION: [Params.COMPUTE_CLASSIFICATION_METRICS],
                                TrainerTask.TRAIN: [Params.MODEL_SUFFIX, Params.N_EPOCHS, Params.LEARNING_RATE_MULTIPLIER],
                                TrainerTask.PREDICT: [Params.TEMPERATURE, Params.MAX_TOKENS, Params.LOG_PROBS]}

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
        prompt = params.get(OpenAiUtil.Params.PROMPT)
        batches = ListUtil.batch(prompt, n=OpenAiUtil.MAX_COMPLETION_PROMPTS) if isinstance(prompt, list) else [prompt]
        res = None
        for batch in batches:
            params[OpenAiUtil.Params.PROMPT] = batch
            batch_res = openai.Completion.create(**params)
            if res is None:
                res = batch_res
            else:
                res.choices.extend(batch_res.choices)
        return res

    @staticmethod
    def upload_file(**params) -> OpenAIObject:
        """
        Makes a request to upload a file
        :param params: Params necessary for request
        :return: The response from open  ai
        """
        return openai.File.create(**params)

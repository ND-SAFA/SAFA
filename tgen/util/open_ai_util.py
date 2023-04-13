from tgen.constants import OPEN_AI_ORG, OPEN_AI_KEY, IS_TEST
import openai

if not IS_TEST:
    assert OPEN_AI_ORG and OPEN_AI_KEY, f"Must supply value for {f'{OPEN_AI_ORG=}'.split('=')[0]} " \
                                        f"and {f'{OPEN_AI_KEY=}'.split('=')[0]} in .env"
    openai.organization = OPEN_AI_ORG
    openai.api_key = OPEN_AI_KEY


class OpenAiUtil:

    @staticmethod
    def make_fine_tune_request(**params):
        return openai.FineTune.create(**params)
    
    @staticmethod
    def retrieve_fine_tune_request(**params):
        return openai.FineTune.retrieve(**params)

    @staticmethod
    def make_completion_request(**params):
        return openai.Completion.create(**params)

    @staticmethod
    def upload_file(**params):
        return openai.File.create(**params)
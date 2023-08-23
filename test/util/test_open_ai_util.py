from tgen.core.args.open_ai_args import OpenAIArgs
from tgen.models.llm.llm_responses import GenerationResponse
from tgen.models.llm.llm_task import LLMCompletionType
from tgen.models.llm.open_ai_manager import OpenAIManager
from tgen.testres.base_tests.base_test import BaseTest
from tgen.testres.mocking.mock_openai import mock_openai
from tgen.testres.mocking.test_response_manager import TestAIManager


class TestOpenAiUtil(BaseTest):
    """
    Tests the OpenAi Utility class.
    """

    @mock_openai
    def test_completion_request(self, ai_manager: TestAIManager):
        n_prompts = 30
        ai_manager.set_responses(["res"] * n_prompts)
        llm_manager = OpenAIManager(OpenAIArgs())

        res: GenerationResponse = llm_manager.make_completion_request(
            completion_type=LLMCompletionType.GENERATION, prompt=["prompt" for i in range(n_prompts)])
        self.assertEqual(len(res.batch_responses), n_prompts)

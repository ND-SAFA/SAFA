from tgen.models.llm.anthropic_manager import AnthropicManager
from tgen.models.llm.llm_responses import GenerationResponse
from tgen.models.llm.llm_task import LLMCompletionType
from tgen.models.llm.open_ai_manager import OpenAIManager
from tgen.testres.base_tests.base_test import BaseTest
from tgen.testres.mocking.mock_anthropic import mock_anthropic
from tgen.testres.mocking.mock_openai import mock_openai
from tgen.testres.mocking.test_response_manager import TestAIManager


class TestLLMUtil(BaseTest):
    """
    Tests the OpenAi Utility class.
    """

    @mock_openai
    def test_open_ai_completion_request_with_retries(self, ai_manager: TestAIManager):
        llm_manager = OpenAIManager()
        self._assert_completion_request_with_retries(llm_manager=llm_manager, ai_manager=ai_manager)

    @mock_anthropic
    def test_completion_requestion_with_retries(self, ai_manager: TestAIManager):
        llm_manager = AnthropicManager()
        self._assert_completion_request_with_retries(llm_manager=llm_manager, ai_manager=ai_manager)

    def _assert_completion_request_with_retries(self, llm_manager, ai_manager: TestAIManager):
        n_prompts = 30
        exception = 5
        ai_manager.set_responses(["res" if i != exception else self.bad_completion for i in range(n_prompts + 1)])

        original_res: GenerationResponse = llm_manager.make_completion_request(
            raise_exception=False,
            completion_type=LLMCompletionType.GENERATION, prompt=["prompt" for i in range(n_prompts)])
        self.assertEqual(len(original_res.batch_responses), n_prompts)

        res: GenerationResponse = llm_manager.make_completion_request(
            raise_exception=False,
            original_responses=original_res.batch_responses,
            completion_type=LLMCompletionType.GENERATION, prompt=["prompt" for i in range(n_prompts)])
        for r in res.batch_responses:
            self.assertEqual(r, "res")

    def bad_completion(self, prompt, **kwargs):
        raise Exception("fake exception")

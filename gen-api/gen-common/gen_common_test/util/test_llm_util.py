import json

from gen_common.llm.anthropic_manager import AnthropicManager
from gen_common.llm.llm_responses import GenerationResponse
from gen_common.llm.llm_task import LLMCompletionType
from gen_common.llm.prompts.prompt import Prompt
from gen_common.llm.prompts.prompt_builder import PromptBuilder
from gen_common.llm.response_managers.json_response_manager import JSONResponseManager
from gen_common.util.llm_util import LLMUtil
from gen_common_test.base.mock.decorators.anthropic import mock_anthropic
from gen_common_test.base.mock.test_ai_manager import TestAIManager
from gen_common_test.base.tests.base_test import BaseTest


class TestLLMUtil(BaseTest):
    """
    Tests the OpenAi Utility class.
    """

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

    @mock_anthropic
    def test_complete_iterable_prompts(self, ai_manager: TestAIManager):
        """
        Tests that complete_iterable_prompts is able to complete a simple use case.
        """
        TEST_JSON_KEY = "response"
        TEST_JSON_VALUE = "test"
        expected_response = json.dumps({TEST_JSON_KEY: TEST_JSON_VALUE})

        llm_manager = AnthropicManager()
        ai_manager.set_responses([expected_response])

        def generator(item):
            builder = PromptBuilder([
                Prompt(item, response_manager=JSONResponseManager(response_tag=TEST_JSON_KEY))
            ])
            prompt = builder.build(llm_manager.prompt_args)
            return builder, prompt

        output = LLMUtil.complete_iterable_prompts(
            items=["test_id"],
            prompt_generator=generator,
            llm_manager=AnthropicManager()
        )

        self.assertEqual(1, len(output))
        parsed_response = output[0][1]
        self.assertIn(TEST_JSON_KEY, parsed_response)
        self.assertEqual(TEST_JSON_VALUE, parsed_response[TEST_JSON_KEY][0])

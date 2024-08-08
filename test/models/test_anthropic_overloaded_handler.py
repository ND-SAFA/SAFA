from unittest.mock import MagicMock

import httpx
from anthropic import InternalServerError

from tgen.common.util.thread_util import ThreadUtil
from tgen.models.llm.anthropic_overloaded_handler import anthropic_overloaded_handler
from tgen.testres.base_tests.base_test import BaseTest
from tgen.testres.mocking.mock_anthropic import mock_anthropic
from tgen.testres.mocking.test_response_manager import TestAIManager

MOCK_ANTHROPIC_OVERLOADED_RESPONSE = {
    "type": "error",
    "error": {"type": "overloaded_error", "message": "Overloaded"}
}


class TestAnthropicOverloadedHandler(BaseTest):
    @mock_anthropic
    def test_overloaded(self, ai_manager: TestAIManager):
        """
        Tests that when the server is overloaded, the thread manager responds accordingly.
        """
        # Define the mocked request
        ai_manager.add_responses(["Hi, my name is Claude."])
        mock_request = MagicMock(spec=httpx.Request)
        response = httpx.Response(
            status_code=529,
            json=MOCK_ANTHROPIC_OVERLOADED_RESPONSE,
            request=mock_request
        )

        state = {"i": 0}

        def thread_word(work):
            if state["i"] == 1:
                state["i"] += 1
                raise InternalServerError(message="This is the message", response=response, body=MOCK_ANTHROPIC_OVERLOADED_RESPONSE)
            else:
                state["i"] += 1

        state = ThreadUtil.multi_thread_process(title="Testing Overloaded Errors",
                                                iterable=[1, 2, 3, 4],
                                                thread_work=thread_word,
                                                n_threads=4,
                                                sleep_time=0.01,
                                                max_attempts=3,
                                                exception_handlers=[anthropic_overloaded_handler])

        self.assertTrue(state.successful)

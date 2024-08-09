from unittest.mock import MagicMock

import httpx
from anthropic import InternalServerError

from tgen.common.util.thread_util import ThreadUtil
from tgen.models.llm.anthropic_exception_handler import anthropic_exception_handler
from tgen.testres.base_tests.base_test import BaseTest
from tgen.testres.mocking.mock_anthropic import mock_anthropic
from tgen.testres.mocking.test_response_manager import TestAIManager

MOCK_ANTHROPIC_OVERLOADED_RESPONSE = {
    "type": "error",
    "error": {"type": "overloaded_error", "message": "Overloaded"}
}


class TestAnthropicOverloadedHandler(BaseTest):
    @mock_anthropic
    def test_anthropic_exception_handler(self, ai_manager: TestAIManager):
        """
        Tests that when the server is overloaded, the thread manager responds accordingly.
        ---
        Below, we are performing a batch job where one of the threads throws an Anthropic InternalServerError.

        I have set the maximum number of attempts to 1, meaning, that if this error is caught successfully then
        the handler successfully intercepted the exception and handled it. Notabely, the AI manager will check that
        the handler does indeed call anthropic to check its availability before returning back to retry the request.
        """
        # Define the mocked request
        ai_manager.add_responses(["Hi, my name is Claude."])
        state = {"i": 0}

        def thread_word(work):
            if state["i"] == 1:
                state["i"] += 1
                raise InternalServerError(message="This is the message",
                                          response=httpx.Response(
                                              status_code=529,
                                              json=MOCK_ANTHROPIC_OVERLOADED_RESPONSE,
                                              request=MagicMock(spec=httpx.Request)
                                          ),
                                          body=MOCK_ANTHROPIC_OVERLOADED_RESPONSE)
            else:
                state["i"] += 1

        state = ThreadUtil.multi_thread_process(title="Testing Overloaded Errors",
                                                iterable=[1, 2, 3, 4],
                                                thread_work=thread_word,
                                                n_threads=4,
                                                sleep_time=0.01,
                                                max_attempts=1,
                                                exception_handlers=[anthropic_exception_handler],
                                                rpm=60)

        self.assertTrue(state.successful)

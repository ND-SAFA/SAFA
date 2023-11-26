from unittest.mock import Mock, patch

from api.endpoints import async_endpoint
from api.endpoints.endpoint import endpoint
from tgen.testres.mocking.mock_anthropic import mock_anthropic
from tgen.testres.mocking.test_response_manager import TestAIManager


def mock_async(test_function):
    """
    Mocks asynchronous endpoints and converts them to synchronous ones.
    :param test_function: The test method being mocked.
    :return: Decorator with mocked async endpoint decorator.
    """

    @patch.object(async_endpoint, "async_endpoint")
    @mock_anthropic
    def decorator(test_class, test_manager: TestAIManager, mock_async_decorator: Mock):
        """
        Decorates the test case wrapped by outer function with mocked tasked and AI manager.
        :param test_class: The test case of the testing method being run.
        :param test_manager: The test manager responsible for mocking calls.
        :param mock_async_decorator: The async decorator mock that converts it to a syncronous one.
        :return: The output of the test method.
        """
        mock_async_decorator.side_effect = endpoint
        return test_function(test_class, test_manager)

    return decorator

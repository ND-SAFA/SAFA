from tgen.testres.testprojects.mocking.library_formatters import openai_response_formatter
from tgen.testres.testprojects.mocking.mock_ai_decorator import mock_ai
from tgen.testres.testprojects.mocking.test_response_manager import TestAIManager


def mock_openai(func=None, *args, **kwargs):
    """
    Mocks openai response and allows test function to receive a TestResponseManager.
    :param func: Internal. The test function being wrapped.
    :param args: Positional arguments to mock ai decorator.
    :param kwargs: Keyword arguments to mock ai decorator.
    :return: Wrapped test function.
    """

    ai_manager = TestAIManager("openai", openai_response_formatter)
    return mock_ai(libraries="openai", ai_managers=ai_manager, func=func, *args, **kwargs)

from tgen.testres.testprojects.mocking.library_formatters import anthropic_response_formatter
from tgen.testres.testprojects.mocking.mock_ai_decorator import mock_ai
from tgen.testres.testprojects.mocking.test_response_manager import TestAIManager


def mock_anthropic(func=None, *args, **kwargs):
    ai_manager = TestAIManager("anthropic", anthropic_response_formatter)
    return mock_ai(libraries="anthropic", ai_managers=ai_manager, func=func, *args, **kwargs)

from common_resources.mocking.mock_ai_decorator import mock_ai


def mock_libraries(func=None, *args, **kwargs):
    return mock_ai(libraries=["anthropic", "openai"], func=func, *args, **kwargs)

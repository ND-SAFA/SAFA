from gen_common_test.base.mock.decorators.ai import mock_ai


def mock_libraries(func=None, *args, **kwargs):
    return mock_ai(libraries=["anthropic", "openai"], func=func, *args, **kwargs)

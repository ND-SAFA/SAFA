from gen_common_test.base.mock.decorators.mock_ai import mock_ai


def mock_anthropic(func=None, *args, **kwargs):
    return mock_ai(libraries="anthropic", func=func, *args, **kwargs)

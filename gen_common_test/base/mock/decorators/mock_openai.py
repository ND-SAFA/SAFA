from gen_common_test.base.mock.decorators.mock_ai import mock_ai


def mock_openai(func=None, *args, **kwargs):
    """
    Mocks openai response and allows test function to receive a TestResponseManager.
    :param func: Internal. The test function being wrapped.
    :param args: Positional arguments to mock ai decorator.
    :param kwargs: Keyword arguments to mock ai decorator.
    :return: Wrapped test function.
    """
    return mock_ai(libraries="openai", func=func, *args, **kwargs)

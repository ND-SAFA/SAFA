from tgen.testres.mocking.mock_ai_decorator import mock_ai


class MockAnthropicClient:
    """
    Shell for the anthropic client.
    """

    class messages:

        def create(self, *args, **kwargs):
            raise NotImplementedError("This object was access before mocking.")


def mock_anthropic(func=None, *args, **kwargs):
    return mock_ai(libraries="anthropic", func=func, *args, **kwargs)

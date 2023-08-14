from tgen.testres.testprojects.mocking.mock_ai_decorator import mock_ai


class MockAnthropicClient:
    """
    Shell for the anthropic client.
    """

    def completion(self):
        raise NotImplementedError("This object was access before mocking.")


def mock_anthropic(func=None, *args, **kwargs):
    return mock_ai(libraries="anthropic", func=func, *args, **kwargs)

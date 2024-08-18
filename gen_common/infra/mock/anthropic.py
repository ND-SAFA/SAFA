class MockAnthropicClient:
    """
    Shell for the anthropic client.
    """

    class messages:

        def create(self, *args, **kwargs):
            raise NotImplementedError("This object was access before mocking.")

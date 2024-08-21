class MockAnthropicClient:
    """
    Shell for the anthropic client.
    """

    class messages:

        def create(self, *args, **kwargs):
            """
            Creates new messge.
            """
            raise NotImplementedError("This object was access before mocking.")

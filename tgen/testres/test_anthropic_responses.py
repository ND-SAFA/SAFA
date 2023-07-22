from typing import List

from tgen.common.util.attr_dict import AttrDict
from tgen.testres.test_open_ai_responses import mock_ai


def mock_anthropic(func=None, *args, **kwargs):
    def process(responses: List[str]):
        n_responses = len(responses)
        if 0 == n_responses or n_responses > 1:
            raise ValueError("Expected single response from anthropic.")
        response = responses[0]
        res = AttrDict({"completion": response})
        return res

    return mock_ai(library="anthropic", response_formatter=process, func=func, *args, **kwargs)


def mock_openai(func=None, *args, **kwargs):
    """
    Mocks openai response and allows test function to receive a TestResponseManager.
    :param func: Internal. The test function being wrapped.
    :param args: Positional arguments to mock ai decorator.
    :param kwargs: Keyword arguments to mock ai decorator.
    :return: Wrapped test function.
    """

    def process(responses: List[str]):
        res = AttrDict({"choices": [AttrDict({"message": {"content": r}}) for r in responses], "id": "id"})
        return res

    return mock_ai(library="openai", response_formatter=process, func=func, *args, **kwargs)

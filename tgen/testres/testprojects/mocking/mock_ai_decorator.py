from typing import Callable, List
from unittest import mock

from tgen.common.util.attr_dict import AttrDict
from tgen.testres.testprojects.mocking.test_open_ai_responses import does_accept, library_map
from tgen.testres.testprojects.mocking.test_response_manager import TestResponseManager


def mock_ai(library: str, response_formatter: Callable, func=None, format: str = None, test_expected_responses: bool = True,
            *outer_args,
            **outer_kwargs):
    """
    Automatically mocks open ai
    :param format: The format to encapsulate responses in.
    :return: The decorated function with open ai mocked.
    """
    library_mock_string = library_map[library]

    def decorator(test_func: Callable, *test_func_args, **test_func_kwargs):
        @mock.patch(library_mock_string)
        def wrapper(self, mock_completion):
            response_manager = TestResponseManager(format=format, response_formatter=response_formatter, *test_func_args, *outer_args,
                                                   **test_func_kwargs, **outer_kwargs)
            mock_completion.side_effect = response_manager
            if does_accept(test_func, response_manager):
                test_func(self, response_manager)
            else:
                test_func(self)
            if test_expected_responses:
                n_used = response_manager.start_index
                n_expected = len(response_manager.responses)
                assert n_used == n_expected, f"Response manager had {n_expected - n_used} / {n_expected} unused responses."

        function_name = test_func.__name__ if hasattr(test_func, "__name__") else func.__name__
        wrapper.__name__ = function_name
        return wrapper

    return decorator


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

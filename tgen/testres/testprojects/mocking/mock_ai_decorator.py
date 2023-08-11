from typing import Callable, List
from unittest import mock

from tgen.common.util.attr_dict import AttrDict
from tgen.testres.testprojects.mocking.test_open_ai_responses import does_accept, method_mock_map
from tgen.testres.testprojects.mocking.test_response_manager import TestAIManager


def mock_ai(library: str, response_formatter: Callable, func=None, format: str = None, test_expected_responses: bool = True,
            *outer_args,
            **outer_kwargs):
    """
    Automatically mocks open ai
    :param format: The format to encapsulate responses in.
    :return: The decorated function with open ai mocked.
    """
    library_mock_method_name = method_mock_map[library]

    def decorator(test_func: Callable = None, *test_func_args, **test_func_kwargs):

        @mock.patch(library_mock_method_name)
        def test_function_wrapper(self, mock_completion):
            response_manager = TestAIManager(library, response_formatter, format=format,
                                             *outer_args, **outer_kwargs)
            mock_completion.side_effect = response_manager
            if does_accept(test_func, response_manager):
                test_func(self, response_manager, *test_func_args, **test_func_kwargs)
            else:
                test_func(self, *test_func_args, **test_func_kwargs)
            if test_expected_responses:
                n_used = response_manager.start_index
                n_expected = len(response_manager.responses)
                assert n_used == n_expected, f"Response manager had {n_expected - n_used} / {n_expected} unused responses."

        function_name = test_func.__name__ if hasattr(test_func, "__name__") else func.__name__
        test_function_wrapper.__name__ = function_name
        if callable(func):  # allows you to use @mock_anthropic or @mock_anthropic()
            parent_object = test_func
            test_func = func
            return test_function_wrapper(parent_object)
        else:
            return test_function_wrapper

    return decorator


def mock_anthropic(func=None, *args, **kwargs):
    def anthropic_response_formatter(responses: List[str]):
        assert isinstance(responses, list), "Expected list as response from anthropic mock."
        assert len(responses) == 1, "Expected single response in anthropic responses."
        res = AttrDict({"completion": responses[0]})
        return res

    return mock_ai(library="anthropic", response_formatter=anthropic_response_formatter, func=func, *args, **kwargs)


def mock_openai(func=None, *args, **kwargs):
    """
    Mocks openai response and allows test function to receive a TestResponseManager.
    :param func: Internal. The test function being wrapped.
    :param args: Positional arguments to mock ai decorator.
    :param kwargs: Keyword arguments to mock ai decorator.
    :return: Wrapped test function.
    """

    def openai_response_formatter(responses: List[str]):
        res = AttrDict({"choices": [AttrDict({"message": {"content": r}}) for r in responses], "id": "id"})
        return res

    return mock_ai(library="openai", response_formatter=openai_response_formatter, func=func, *args, **kwargs)

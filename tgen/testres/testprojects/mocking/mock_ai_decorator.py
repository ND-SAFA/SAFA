from typing import Callable, List, Union
from unittest.mock import patch

from tgen.testres.testprojects.mocking.test_open_ai_responses import library_formatter_map, library_mock_map
from tgen.testres.testprojects.mocking.test_response_manager import TestAIManager


def mock_ai(libraries: Union[str, List[str]],
            ai_managers: List[TestAIManager],
            func=None):
    """
    Mocks the given library with the ai_manager.
    :param libraries: The library to mock (e.g. anthropic, openai).
    :param ai_managers: The AI manager to intercept call with.
    :param func: The function being decorated.
    :return:
    """
    if isinstance(libraries, str):
        libraries = [libraries]
    if isinstance(ai_managers, TestAIManager):
        ai_managers = [ai_managers]

    library_method_names = [library_mock_map[l] for l in libraries]
    library_ai_managers = [TestAIManager(l, library_formatter_map[l]) for l in libraries]

    def decorator(test_func: Callable = None, *test_func_args, **test_func_kwargs):

        def test_function_wrapper(mock_completion, *wrapper_args, **wrapper_kwargs):
            mock_completion.side_effect = ai_managers
            self, *wrapper_args = wrapper_args
            test_func(self, *library_ai_managers, *test_func_args, *wrapper_args, **test_func_kwargs, **wrapper_kwargs)
            for ai_manager in ai_managers:
                n_used = ai_manager.start_index
                n_expected = len(ai_manager._responses)
                assert n_used == n_expected, f"Response manager had {n_expected - n_used} / {n_expected} unused responses."

        function_name = test_func.__name__ if hasattr(test_func, "__name__") else func.__name__
        test_function_wrapper.__name__ = function_name
        if callable(func):  # allows you to use @mock_anthropic or @mock_anthropic()
            parent_object = test_func
            test_func = func
            return run_with_patches(library_method_names, test_function_wrapper, parent_object)
        else:
            def inner_thing():
                run_with_patches(library_method_names, test_function_wrapper, parent_object)

            return inner_thing

    return decorator


def run_with_patches(patches, runnable: Callable, *args, **kwargs):
    assert len(patches) > 0, f"No methods to patch."
    if len(patches) == 1:
        patch_name = patches[0]
        with patch(patch_name) as other_func:
            runnable(other_func, *args, **kwargs)
    else:
        with patch(patches) as other_func:
            run_with_patches(patches[1:], runnable, other_func, **kwargs)

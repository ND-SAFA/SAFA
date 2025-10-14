from typing import Callable, List, Union
from unittest.mock import patch

from gen_common_test.base.mock.test_ai_manager import TestAIManager
from gen_common_test.base.mock.mocking_config import library_formatter_map, library_mock_map


def mock_ai(libraries: Union[str, List[str]], func=None):
    """
    Mocks the given library with the ai_manager.
    :param libraries: The library to mock (e.g. anthropic, openai).
    :param func: The function being decorated.
    :return:
    """
    if isinstance(libraries, str):
        libraries = [libraries]

    library_method_names = [library_mock_map[l] for l in libraries]
    library_ai_managers = [TestAIManager(l, library_formatter_map[l]) for l in libraries]

    def decorator(test_func: Callable = None, *test_func_args, **test_func_kwargs):

        def test_function_wrapper(local_managers, *wrapper_args, **wrapper_kwargs):
            self, *local_args = wrapper_args
            res = test_func(self, *local_managers, *test_func_args, *local_args, **test_func_kwargs, **wrapper_kwargs)
            for ai_manager in library_ai_managers:
                ai_manager.on_test_end()
            return res

        function_name = test_func.__name__ if hasattr(test_func, "__name__") else func.__name__
        test_function_wrapper.__name__ = function_name
        if callable(func):  # allows you to use @mock_anthropic or @mock_anthropic()
            parent_object = test_func
            test_func = func
            return run_with_patches(library_method_names, library_ai_managers, test_function_wrapper, parent_object)
        else:
            def inner_thing():
                run_with_patches(library_method_names, library_ai_managers, test_function_wrapper, parent_object)

            return inner_thing

    return decorator


def run_with_patches(patches: List[str], ai_managers, runnable: Callable, *args, **kwargs):
    assert len(patches) > 0, f"No methods to patch."
    patch_name = patches[0]
    if len(patches) == 1:
        with patch(patch_name) as other_func:
            other_func.side_effect = ai_managers[-1]
            return runnable(ai_managers, *args, **kwargs)
    else:
        with patch(patch_name) as other_func:
            other_func.side_effect = ai_managers[0]
            return run_with_patches(patches[1:], ai_managers, runnable, *args, **kwargs)

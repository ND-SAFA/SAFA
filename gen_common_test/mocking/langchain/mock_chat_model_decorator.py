from typing import Callable
from unittest.mock import patch

from gen_common.graph.agents.base_agent import BaseAgent

from gen_common_test.mocking.langchain.test_chat_model import TestResponseManager
from gen_common.util.reflection_util import ReflectionUtil

PATCH_OBJ = BaseAgent._create_model
PATCH_PATH = ReflectionUtil.get_obj_full_path(PATCH_OBJ)


def mock_chat_model(func=None):
    def decorator(test_func: Callable = None, *test_func_args, **test_func_kwargs):

        def test_function_wrapper(local_managers, *wrapper_args, **wrapper_kwargs):
            self, *local_args = wrapper_args
            res = test_func(self, *local_managers, *test_func_args, *local_args, **test_func_kwargs, **wrapper_kwargs)
            return res

        function_name = test_func.__name__ if hasattr(test_func, "__name__") else func.__name__
        test_function_wrapper.__name__ = function_name
        if callable(func):  # allows you to use @mock_anthropic or @mock_anthropic()
            parent_object = test_func
            test_func = func
            return run_with_patches(test_function_wrapper, parent_object)
        else:
            def inner_thing():
                run_with_patches(test_function_wrapper, parent_object)

            return inner_thing

    return decorator


def run_with_patches(runnable: Callable, *args, **kwargs):
    with patch(PATCH_PATH) as other_func:
        chat_model = TestResponseManager()
        other_func.side_effect = chat_model
        return runnable([chat_model], *args, **kwargs)

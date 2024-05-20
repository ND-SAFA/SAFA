from typing import Any, Set, Optional

from tgen.common.util.param_specs import ParamSpecs
from tgen.common.util.reflection_util import ReflectionUtil

MUTABLE_TYPES = {set, list, dict}

"""
A util to deal with #justpythonthings that desperately need utils to deal with them
since the python creators couldn't be bothered.
"""


def is_allowed_to_be_none(param_name: str, allowed_none: Optional[Set]) -> bool:
    """
    Returns True if the param can be None.
    :param param_name: The name of the param.
    :param allowed_none: A set of params that are allowed to be None.
    :return: True if the param can be None else False.
    """
    if allowed_none is None:
        return False
    return param_name in allowed_none


def default_mutable(allowed_none: Set[str] = None) -> Any:
    """
    Decorator for setting the default value of all mutable params in method.
    :param allowed_none: Set of mutable parameters that should remain None.
    :return: The result of the function
    """

    def decorator(func):
        """
        Defines the python decorator for a function with mutable default params.
        :param func: The function with mutable default params
        :return: The result of the function.
        """

        def wrapper(*args, **kwargs):
            """
            Defines the logic that sets all mutable type defaults to be the expected type.
            :param args: Args to the function.
            :param kwargs: Kwargs to the function.
            :return: Result of the function.
            """
            specs = ParamSpecs.create_from_method(func)
            kwargs.update(specs.convert_args_to_kwargs(args))
            for param_name, expected_type in specs.param_types.items():
                try:
                    if param_name in specs.required_params:
                        continue
                    if kwargs.get(param_name, None) is None and not is_allowed_to_be_none(param_name, allowed_none):
                        for mutable_type in MUTABLE_TYPES:
                            if ReflectionUtil.is_type(mutable_type(), expected_type, param_name, print_on_error=False):
                                kwargs[param_name] = mutable_type()
                                break
                except Exception as e:
                    print("uhuh")
                    continue

            return func(**kwargs)

        return wrapper

    return decorator

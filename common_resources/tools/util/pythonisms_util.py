from typing import Any, Dict, List, Optional, Set, Type

from common_resources.tools.util.param_specs import ParamSpecs
from common_resources.tools.util.reflection_util import ReflectionUtil

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


def default_mutable_type(expected_type: Type) -> Set | Dict | List | None:
    """
    If expected type is a mutable type (i.e. list, set, dict), initializes an empty object of that type.
    :param expected_type: The expected type.
    :return: An empty object of that type if mutable else None.
    """
    for mutable_type in MUTABLE_TYPES:
        if ReflectionUtil.is_type(mutable_type(), expected_type, print_on_error=False):
            return mutable_type()


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
                        default = default_mutable_type(expected_type)
                        if default is not None:
                            kwargs[param_name] = default
                except Exception as e:
                    continue

            return func(**kwargs)

        return wrapper

    return decorator


MUTABLE_TYPES = {set, list, dict}

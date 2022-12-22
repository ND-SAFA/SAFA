from abc import ABC
from copy import copy
from dataclasses import dataclass
from typing import Any, Type, get_type_hints, _SpecialGenericAlias, Union, Dict, Callable, Set, Optional, _UnionGenericAlias, \
    _Final, _GenericAlias, _CallableGenericAlias, _CallableType, get_origin, get_args, List, Tuple
from experiments.variables.variable import Variable

from experiments.variables.definition_variable import DefinitionVariable
from inspect import isfunction, getfullargspec


@dataclass
class ParamSpecs:
    param_names: Set[str]
    param_types: Dict[str, Union[Type, _SpecialGenericAlias]]
    has_kwargs: bool
    required_params: Set[str]


class BaseObject(ABC):

    # TODO add None with optional case
    # TODO clean up _is_instance

    @classmethod
    def initialize_from_definition(cls, definition: DefinitionVariable):
        """
        Initializes the object from a dictionary
        :param definition: a dictionary of the necessary params to initialize
        :return: the initialize object
        """
        param_specs = ParamSpecs.create_from_method(cls.__init__)
        param_specs.assert_definition(definition)

        params = {}
        for param_name, variable in definition.items():
            expected_type = param_specs.param_types[param_name] if param_name in param_specs.param_types else None
            param_value = cls._get_value_of_variable(variable, expected_type)
            if expected_type:
                cls._assert_type(param_value, expected_type, param_name)
            params[param_name] = param_value
        return cls(**params)

    @classmethod
    def _get_value_of_variable(cls, variable: Union[Variable, Any], expected_type: Union[Type, _SpecialGenericAlias] = None) -> Any:
        """
        Gets the value of a given variable
        :param variable: the variable, can be any variable class or the actual value desired
        :param expected_type: the expected type for the value
        :return: the value
        """
        val = variable
        if isinstance(variable, DefinitionVariable):
            val = cls._make_child_object(variable, expected_type) if expected_type else None
        elif isinstance(variable, Variable):
            val = variable.value
        return val

    @classmethod
    def _make_child_object(cls, definition: DefinitionVariable, expected_class: Type) -> Any:
        """
        Handles making children objects
        :param expected_class: the expected_class for the child object
        :param definition: contains attributes necessary to construct the child
        :return: the child object
        """
        if isinstance(expected_class, BaseObject):
            return expected_class.initialize_from_definition(definition)

        params = {param_name: cls._get_value_of_variable(variable)
                  for param_name, variable in definition.items()}
        try:
            return expected_class(**params)
        except Exception as e:
            raise TypeError("Unable to initialize %s for %s" % (expected_class, cls.__name__))

    @classmethod
    def _assert_type(cls, val: Any, expected_type: Union[Type, _SpecialGenericAlias], param_name: str):
        """
        Asserts that the value is of the expected type for the variable with the given name
        :param val: the value
        :param expected_type: expected type or typing generic
        :param param_name: the name of the parameter being tested
        :return: None (raises an exception if not the expected type)
        """

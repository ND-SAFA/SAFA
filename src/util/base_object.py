from abc import ABC, abstractmethod
from copy import copy
from dataclasses import dataclass
from typing import Any, Type, get_type_hints, List, _SpecialGenericAlias, Union, Dict, Callable, Set, Optional, _UnionGenericAlias, \
    _Final
from experiments.variables.variable import Variable

from experiments.variables.definition_variable import DefinitionVariable
import inspect


@dataclass
class ParamSpecs:
    param_names: Set[str]
    param_types: Dict[str, Union[Type, _SpecialGenericAlias]]
    has_kwargs: bool
    required_params: Set[str]


class BaseObject(ABC):

    @classmethod
    def initialize_from_definition(cls, definition: DefinitionVariable):
        """
        Initializes the object from a dictionary
        :param definition: a dictionary of the necessary params to initialize
        :return: the initialize object
        """
        param_specs = cls._get_param_specs(cls.__init__)
        cls._assert_no_missing_params(definition, param_specs)
        cls._assert_no_unexpected_params(definition, param_specs)

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
        if not cls._is_instance(val, expected_type):
            raise TypeError("%s expected type %s for %s but received %s" % (cls.__name__, expected_type, param_name, type(val)))

    @classmethod
    def _assert_no_missing_params(cls, definition: Dict, param_specs: ParamSpecs) -> None:
        """
        Asserts that there are no missing params for the method represented by the given param specs
        :param definition: the dictionary of parameter name to value mappings to check
        :param param_specs: the parameter specs for the method
        :return: None (raises an exception if there are missing params)
        """
        missing_params = cls._get_any_missing_required_params(definition, param_specs)
        if len(missing_params) >= 1:
            raise TypeError("%s is missing required arguments: %s" % (cls.__name__, missing_params))

    @classmethod
    def _assert_no_unexpected_params(cls, definition: Dict, param_specs: ParamSpecs) -> None:
        """
        Asserts that there are no unexpected params for the method represented by the given param specs
        :param definition: the dictionary of parameter name to value mappings to check
        :param param_specs: the parameter specs for the method
        :return: None (raises an exception if there are unexpected params)
        """
        extra_params = cls._get_any_additional_params(definition, param_specs)
        if len(extra_params) >= 1 and not param_specs.has_kwargs:
            raise TypeError("%s received unexpected arguments: %s" % (cls.__name__, extra_params))

    @staticmethod
    def _get_any_missing_required_params(param_dict: Dict, param_specs: ParamSpecs) -> Set[str]:
        """
        Gets any missing params for the given param specs that are not supplied in the parameter dictionary
        :param param_dict: the dictionary of parameter name to value mappings to check
        :param param_specs: the parameter specs for the method to check if all required params have been supplied
        :return: a set of any missing required parameters
        """
        return set(param_specs.required_params).difference(set(param_dict.keys()))

    @staticmethod
    def _get_any_additional_params(param_dict: Dict, param_specs: ParamSpecs) -> Set[str]:
        """
        Gets any additional params for the given param specs that are supplied in the parameter dictionary
        :param param_dict: the dictionary of parameter name to value mappings to check
        :param param_specs: the parameter specs for the method to get any additional parameters for
        :return: a set of any additional parameters
        """
        return set(param_dict.keys()).difference(param_specs.param_names)

    @staticmethod
    def _is_instance(val: Any, expected_type: Union[Type, _SpecialGenericAlias]) -> bool:
        """
        Determines that the value is of the correct type
        :param val: the value
        :param expected_type: expected type or typing generic
        :return: True if value is the expected type else False
        """
        if isinstance(expected_type, _UnionGenericAlias):
            is_instance = False
            for child_type in expected_type.__args__:
                if child_type is not None:
                    is_instance = is_instance or BaseObject._is_instance(val, child_type)
            return is_instance
        else:
            if isinstance(expected_type, _SpecialGenericAlias):
                expected_type = expected_type.__origin__
            return isinstance(val, expected_type)

    @staticmethod
    def _get_param_specs(method: Callable) -> ParamSpecs:
        """
        Returns the param specs for the given method
        :param method: the method to create param specs for
        :return: the param specs
        """
        full_specs = inspect.getfullargspec(method)
        expected_param_names = full_specs.args
        expected_param_names.remove("self")

        param_names = set(copy(expected_param_names))
        type_hints = get_type_hints(method)
        param_types = {param: type_hints[param] if param in type_hints else None for param in param_names}

        expected_param_names.reverse()
        required_params = {param for i, param in enumerate(expected_param_names)
                           if full_specs.defaults and i >= len(full_specs.defaults)}

        return ParamSpecs(param_names=param_names, param_types=param_types,
                          required_params=required_params, has_kwargs=full_specs.varkw is not None)

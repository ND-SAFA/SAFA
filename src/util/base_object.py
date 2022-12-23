from abc import ABC
from typing import Any, Type, Union

from typeguard import check_type

from experiments.variables.definition_variable import DefinitionVariable
from experiments.variables.multi_variable import MultiVariable
from experiments.variables.typed_variable import TypedVariable
from experiments.variables.variable import Variable
from util.param_specs import ParamSpecs


class BaseObject(ABC):

    # TODO currently cannot handle a list of definition variables (see below):
    #     DataCleaner.initialize_from_definition(
    #         DefinitionVariable({"steps": Variable([DefinitionVariable({"type": Variable("REMOVE_UNWANTED_CHARS")})])}))

    @classmethod
    def initialize_from_definition(cls, definition: DefinitionVariable):
        """
        Initializes the object from a dictionary
        :param definition: a dictionary of the necessary params to initialize
        :return: the initialized object
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
    def _get_value_of_variable(cls, variable: Union[Variable, Any],
                               expected_type: Union[Type] = None) -> Any:
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
        if expected_class.__name__.startswith("Abstract"):
            if TypedVariable.OBJECT_TYPE_KEY not in definition:
                raise TypeError("Cannot create abstract class. Please specify type to create %s", expected_class)
            expected_class = cls._get_expected_class_for_abstract(expected_class,
                                                                  cls._get_value_of_variable(definition[TypedVariable.OBJECT_TYPE_KEY]))

        if isinstance(expected_class, BaseObject):
            return expected_class.initialize_from_definition(definition)

        params = {param_name: cls._get_value_of_variable(variable)
                  for param_name, variable in definition.items()}
        try:
            return expected_class(**params)
        except Exception as e:
            raise TypeError("Unable to initialize %s for %s" % (expected_class, cls.__name__))

    @classmethod
    def _get_expected_class_for_abstract(cls, abstract_class: Type, child_class_name: str) -> Any:
        """
        *Must be implemented in calling class*
        Returns the correct expected class when given the abstract parent class type and name of child class
        :param abstract_class: the abstract parent class type
        :param child_class_name: the name of the child class
        :return: the expected type
        """
        raise TypeError("Cannot create %s because %s has not defined a creation method.")

    @classmethod
    def _assert_type(cls, val: Any, expected_type: Union[Type], param_name: str):
        """
        Asserts that the value is of the expected type for the variable with the given name
        :param val: the value
        :param expected_type: expected type or typing generic
        :param param_name: the name of the parameter being tested
        :return: None (raises an exception if not the expected type)
        """
        try:
            check_type(param_name, val, expected_type)
        except TypeError:
            raise TypeError(
                "%s expected type %s for %s but received %s" % (cls.__name__, expected_type, param_name, type(val)))
from abc import ABC
from copy import deepcopy
from typing import Any, Dict, List, Type, Union, _UnionGenericAlias, get_args

from typeguard import check_type

from util.enum_utils import get_enum_from_name
from util.param_specs import ParamSpecs
from util.reflection_util import ReflectionUtil
from util.variables.definition_variable import DefinitionVariable
from util.variables.experimental_variable import ExperimentalVariable
from util.variables.multi_variable import MultiVariable
from util.variables.typed_definition_variable import TypedDefinitionVariable
from util.variables.undetermined_variable import UndeterminedVariable
from util.variables.variable import Variable


class BaseObject(ABC):

    def use_values_from_object_for_undetermined(self, obj: "BaseObject") -> None:
        """
        Fills in any undetermined values in self by using values from the given object
        :param obj: the object to use to fill in values
        :return: None
        """
        for attr_name, attr_value in vars(self).items():
            if isinstance(attr_value, UndeterminedVariable):
                if not hasattr(obj, attr_name):
                    raise TypeError("Cannot set undetermined variable because %s does not contain %s"
                                    % (obj.__class__.__name__, attr_name))
                value_to_use = getattr(obj, attr_name)
                setattr(self, attr_name, value_to_use)
            elif isinstance(attr_value, BaseObject):
                obj_to_use = getattr(obj, attr_name)
                attr_value.use_values_from_object_for_undetermined(obj_to_use)

    @classmethod
    def initialize_from_definition(cls, definition: DefinitionVariable):
        """
        Initializes the obj from a dictionary
        :param definition: a dictionary of the necessary params to initialize
        :return: the initialized obj
        """
        param_specs = ParamSpecs.create_from_method(cls.__init__)
        param_specs.assert_definition(definition)

        params_list = [{}]

        for param_name, variable in definition.items():
            expected_type = param_specs.param_types[param_name] if param_name in param_specs.param_types else None
            param_value = cls._get_value_of_variable(variable, expected_type)
            if isinstance(param_value, ExperimentalVariable):
                experiment_params_list = []
                for experiment_val in param_value:
                    experiment_params_list.extend(cls._set_params_values(params_list, param_name, experiment_val))
                params_list = experiment_params_list
            else:
                params_list = cls._set_params_values(params_list, param_name, param_value, expected_type)
        instances = [cls(**params) for params in params_list]
        return instances.pop() if len(instances) == 1 else ExperimentalVariable([Variable(i) for i in instances])

    @classmethod
    def get_generic(cls, expected_type):
        if isinstance(expected_type, _UnionGenericAlias):
            args = get_args(expected_type)
            return args[0]

    @classmethod
    def _get_value_of_variable(cls, variable: Union[Variable, Any], expected_type: Union[Type] = None) -> Any:
        """
        Gets the value of a given variable
        :param variable: the variable, can be any variable class or the actual value desired
        :param expected_type: the expected type for the value
        :return: the value
        """
        if isinstance(variable, UndeterminedVariable):
            val = variable
        elif isinstance(variable, MultiVariable):
            expected_inner_types = get_args(expected_type)
            expected_inner_type = expected_inner_types[0] if len(expected_inner_types) >= 1 else expected_type
            val = []
            for i, inner_var in enumerate(variable):
                expected_inner_type = expected_inner_types[i] if i < len(expected_inner_types) else expected_inner_type
                inner_val = cls._get_value_of_variable(inner_var, expected_inner_type)
                val.append(inner_val)
            if isinstance(variable, ExperimentalVariable):
                val = ExperimentalVariable(val)
        elif isinstance(variable, TypedDefinitionVariable):
            expected_class = cls._get_expected_class_by_type(expected_type, variable.object_type)
            val = cls._make_child_object(DefinitionVariable(variable), expected_class)
        elif isinstance(variable, DefinitionVariable) or isinstance(variable, TypedDefinitionVariable):
            val = cls._make_child_object(variable, expected_type) if expected_type else None
        elif isinstance(variable, Variable):
            val = variable.value
        else:
            val = variable
        return val

    @classmethod
    def _set_params_values(cls, params_list: List[Dict], param_name: str, param_value: Any,
                           expected_type: Type = None) -> List[Dict]:
        """
        Adds the param_name, param_value pair to each params dictionary in the params list
        :param params_list: list of params dictionary
        :param param_name: the name of the new param to add
        :param param_value: the value of the new param to add
        :param expected_type: the expected type of the param value
        :return: the list of params dictionaries with the new param added
        """
        params_list_out = []
        if expected_type:
            cls._assert_type(param_value, expected_type, param_name)
        for params in params_list:
            params_out = deepcopy(params)
            params_out[param_name] = deepcopy(cls._get_value_of_variable(param_value))
            params_list_out.append(params_out)
        return params_list_out

    @classmethod
    def _make_child_object(cls, definition: DefinitionVariable, expected_class: Type) -> Any:
        """
        Handles making children objects
        :param expected_class: the expected_class for the child obj
        :param definition: contains attributes necessary to construct the child
        :return: the child obj
        """
        if ReflectionUtil.is_instance_or_subclass(expected_class, BaseObject):
            return expected_class.initialize_from_definition(definition)

        params = {param_name: cls._get_value_of_variable(variable, expected_class)
                  for param_name, variable in definition.items()}
        try:
            return expected_class(**params)
        except Exception as e:
            raise TypeError("Unable to initialize %s for %s" % (expected_class, cls.__name__))

    @classmethod
    def _get_expected_class_by_type(cls, abstract_class: Type, child_class_name: str) -> Any:
        """
        Returns the correct expected class when given the abstract parent class type and name of child class
        :param abstract_class: the abstract parent class type
        :param child_class_name: the name of the child class
        :return: the expected type
        """
        return get_enum_from_name(cls._get_child_enum_class(abstract_class, child_class_name), child_class_name).value

    @classmethod
    def _get_child_enum_class(cls, abstract_class: Type, child_class_name: str) -> Type:
        """
        Returns the correct enum class mapping name to class given the abstract parent class type and name of child class
        :param abstract_class: the abstract parent class type
        :param child_class_name: the name of the child class
        :return: the enum class mapping name to class
        """
        raise TypeError(
            "Cannot create %s because %s has not defined the enum class to use." % (child_class_name, cls.__name__))

    @classmethod
    def _assert_type(cls, val: Any, expected_type: Union[Type], param_name: str):
        """
        Asserts that the value is of the expected type for the variable with the given name
        :param val: the value
        :param expected_type: expected type or typing generic
        :param param_name: the name of the parameter being tested
        :return: None (raises an exception if not the expected type)
        """
        if isinstance(val, UndeterminedVariable):
            return
        try:
            check_type(param_name, val, expected_type)
        except TypeError:
            raise TypeError(
                "%s expected type %s for %s but received %s" % (cls.__name__, expected_type, param_name, type(val)))

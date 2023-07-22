import traceback
from abc import ABC
from copy import deepcopy
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Type, TypedDict, Union, get_args

from typeguard import check_type
from typing_extensions import get_args

from tgen.common.util.enum_util import get_enum_from_name
from tgen.common.util.logging.logger_manager import logger
from tgen.common.util.param_specs import ParamSpecs
from tgen.common.util.reflection_util import ReflectionUtil
from tgen.variables.definition_variable import DefinitionVariable
from tgen.variables.experimental_variable import ExperimentalVariable
from tgen.variables.multi_variable import MultiVariable
from tgen.variables.typed_definition_variable import TypedDefinitionVariable
from tgen.variables.undetermined_variable import UndeterminedVariable
from tgen.variables.variable import Variable


@dataclass
class ObjectMeta:
    init_params: Dict = field(init=False, default_factory=dict)
    experimental_vars: Dict = field(init=False, default_factory=dict)
    instance: Any = field(init=False)

    def add_param(self, param_name: str, param_val: Any, is_experimental: bool = False,
                  children_experimental_vars: Dict = None) -> None:
        """
        Adds a param to the object meta
        :param param_name: the name of the parameter
        :param param_val: the value of the parameter
        :param is_experimental: True if the parameter is an experimental variable
        :param children_experimental_vars: a dictionary mapping param name to values for all children experiment vars
        :return: None
        """
        self.init_params[param_name] = param_val
        if children_experimental_vars:
            self.experimental_vars.update(children_experimental_vars)
        if is_experimental:
            self.experimental_vars[param_name] = param_val


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

        obj_meta_list = [ObjectMeta()]

        for param_name, variable in definition.items():
            expected_param_type = param_specs.param_types[param_name] if param_name in param_specs.param_types else None
            param_value = cls._get_value_of_variable(variable, expected_param_type)

            if isinstance(param_value, ExperimentalVariable):
                obj_meta_list[0].init_params[param_name] = param_value
                experiment_params_list = []
                for i, inner_variable in enumerate(param_value):
                    inner_variable_value = cls._get_value_of_variable(inner_variable, expected_param_type)

                    children_experimental_vars = param_value.experimental_param2val[i] if param_value.experimental_param2val else {}
                    expanded_params = cls._add_param_values(obj_meta_list=obj_meta_list,
                                                            param_name=param_name,
                                                            param_value=inner_variable_value,
                                                            expected_type=expected_param_type,
                                                            is_experimental=True,
                                                            children_experimental_vars=children_experimental_vars)
                    experiment_params_list.extend(expanded_params)
                obj_meta_list = experiment_params_list
            else:
                obj_meta_list = cls._add_param_values(obj_meta_list, param_name, param_value, expected_param_type)
        instances = []
        for obj_meta in obj_meta_list:
            obj_params = obj_meta.init_params
            new_obj = cls(**obj_params)
            instances.append(new_obj)
        experimental_vars = [obj_meta.experimental_vars for obj_meta in obj_meta_list]
        return instances.pop() if len(instances) == 1 else ExperimentalVariable(instances,
                                                                                experimental_param_name_to_val=experimental_vars)

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
        elif isinstance(variable, ExperimentalVariable):
            val = variable
        elif isinstance(variable, MultiVariable):
            parent_class, *child_classes = ReflectionUtil.get_typed_class(expected_type)
            if parent_class == "optional":
                print("HI")
            elif parent_class == "list":
                if len(child_classes) == 1:
                    expected_child_class = child_classes[0]
                    val = []
                    for v in variable.value:
                        inner_value = cls._get_value_of_variable(v, expected_child_class)
                        if isinstance(inner_value, ExperimentalVariable):  # single item turned t
                            inner_values = [cls._get_value_of_variable(v2, expected_child_class) for v2 in inner_value.value]
                            val.extend(inner_values)
                        else:
                            val.append(inner_value)
                    return val
                else:
                    raise TypeError(f"Found more than possible types in class: {child_classes}")
            elif parent_class == "union":
                list_type = [c for c in child_classes if hasattr(c, "_name") and c._name == "List"]
                if len(list_type) == 0:
                    raise TypeError(f"Multivariable expected type must be some sort of list. Received: {child_classes}")
                val = cls._get_value_of_variable(variable, list_type[0])
                return val
            else:
                raise TypeError(f"Expected {expected_type} to be list or optional but received: {expected_type}.")

        elif isinstance(variable, TypedDefinitionVariable):
            expected_class = cls._get_expected_class_by_type(expected_type, variable.object_type)
            val = cls._make_child_object(DefinitionVariable(variable), expected_class)
        elif isinstance(variable, ExperimentalVariable):
            val = variable
        elif isinstance(variable, DefinitionVariable):
            val = cls._make_child_object(variable, expected_type) if expected_type else None
        elif isinstance(variable, Variable):
            val = variable.value
        else:  # not a variable
            val = variable
        if ReflectionUtil.is_instance_or_subclass(expected_type, Enum) and isinstance(val, str):
            val = get_enum_from_name(expected_type, val)
        return val

    @classmethod
    def _make_child_object(cls, definition: DefinitionVariable, expected_class: Type) -> Any:
        """
        Handles making children objects
        :param expected_class: the expected_class for the child obj
        :param definition: contains attributes necessary to construct the child
        :return: the child obj
        """
        return cls._make_child_object_helper(definition, expected_class)

    @classmethod
    def _make_child_object_helper(cls, definition: DefinitionVariable, expected_class: Type) -> Any:
        """
        Handles the logic to make children objects
        :param expected_class: the expected_class for the child obj
        :param definition: contains attributes necessary to construct the child
        :return: the child obj
        """
        expected_class = ReflectionUtil.get_target_class_from_type(expected_class)
        if ReflectionUtil.is_instance_or_subclass(expected_class, BaseObject):
            return expected_class.initialize_from_definition(definition)

        params = {param_name: cls._get_value_of_variable(variable, expected_class)
                  for param_name, variable in definition.items()}
        try:
            if expected_class in [Dict[str, str], Dict[str, float], Dict[str, int]]:
                # TODO: Add flag to indicate when data should be created as a dictionary of data
                return params
            return expected_class(**params)
        except Exception as e:
            error_msg = f"Unable to initialize {expected_class} for {cls.__name__}."
            traceback.print_exc()
            logger.exception(msg=error_msg)
            raise TypeError(error_msg)

    @classmethod
    def _add_param_values(cls, obj_meta_list: List[ObjectMeta], param_name: str, param_value: Any,
                          expected_type: Type = None, is_experimental: bool = False,
                          children_experimental_vars: Dict = None) -> List[ObjectMeta]:
        """
        Adds the param_name, param_value pair to each params dictionary in the params list
        :param obj_meta_list: list of params dictionary
        :param param_name: the name of the new param to add
        :param param_value: the value of the new param to add
        :param expected_type: the expected type of the param value
        :param is_experimental: True if the new param is an experimental variable
        :param children_experimental_vars: a dictionary mapping param name to values for all children experiment vars
        :return: the list of params dictionaries with the new param added
        """
        obj_meta_list_out = []
        if expected_type:
            cls._assert_type(param_value, expected_type, param_name)
        for obj_meta in obj_meta_list:
            meta_out = deepcopy(obj_meta)
            inner_param_value = cls._get_value_of_variable(param_value, expected_type)
            inner_param_value = deepcopy(inner_param_value)
            meta_out.add_param(param_name, inner_param_value,
                               is_experimental=is_experimental,
                               children_experimental_vars=children_experimental_vars)
            obj_meta_list_out.append(meta_out)
        return obj_meta_list_out

    @classmethod
    def _get_expected_class_by_type(cls, abstract_class: Type, child_class_name: str) -> Any:
        """
        Returns the correct expected class when given the abstract parent class type and name of child class
        :param abstract_class: the abstract parent class type
        :param child_class_name: the name of the child class
        :return: the expected type
        """
        abstract_class = cls._get_base_class(abstract_class)
        assert hasattr(abstract_class, "_get_enum_class"), f"{abstract_class} does not implement `_get_enum_class`"
        enum_class = abstract_class._get_enum_class(child_class_name)
        enum_value = get_enum_from_name(enum_class, child_class_name).value
        return enum_value

    @staticmethod
    def _get_base_class(typing_obj: Any) -> Optional[Type["BaseObject"]]:
        """
        Gets the base object child class nested within a typing object
        :param typing_obj: A typing object
        :return: The base object child class
        """
        children = get_args(typing_obj)
        while len(children) > 0:
            if ReflectionUtil.is_instance_or_subclass(children[0], BaseObject):
                return children[0]
            children = get_args(children[0])
        return typing_obj

    @classmethod
    def _get_enum_class(cls, child_class_name: str) -> Type:
        """
        Returns the correct enum class mapping name to class given the abstract parent class type and name of child class
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
        if not cls._is_type(val, expected_type, param_name):
            raise TypeError(
                "%s expected type %s for %s but received %s" % (cls.__name__, expected_type, param_name, type(val)))

    @classmethod
    def _is_type(cls, val: Any, expected_type: Union[Type], param_name: str, print_on_error: bool = True) -> bool:
        """
        Checks if the value is of the expected type for the variable with the given name
        :param val: the value
        :param expected_type: expected type or typing generic
        :param param_name: the name of the parameter being tested
        :return: True if the type of val matches expected_type, False otherwise
        """
        try:
            if isinstance(val, UndeterminedVariable):
                return True

            if ReflectionUtil.is_typed_dict(expected_type):
                assert isinstance(val, dict)
                for field_name, expected_field_type in expected_type.__annotations__.items():
                    check_type(f"{param_name}-{field_name}", val.get(field_name, None), expected_field_type)
                return True

            if ReflectionUtil.is_typed_class(expected_type):
                expected_type_name = expected_type._name
                if expected_type_name == "Any":
                    return True

                parent_class, *child_classes = ReflectionUtil.get_typed_class(expected_type)
                if parent_class == "dict":
                    expected_type = child_classes[0]
                elif parent_class == "list":
                    child_type = child_classes[0]
                    invalid_runs = [v for v in val if not cls._is_type(v, child_type, param_name, print_on_error=False)]
                    if len(invalid_runs) > 0:
                        raise TypeError(f"List elements {invalid_runs} was not of type {child_type}.")
                    return True
                elif parent_class == "union":
                    queries = [c for c in child_classes if cls._is_type(val, c, param_name, print_on_error=False)]
                    if len(queries) == 0:
                        raise TypeError(f"{val} was not of type: {child_classes}")
                    return True
                elif parent_class == "callable":
                    check_type(param_name, val, expected_type)
                    return True
                else:
                    expected_type = parent_class

            check_type(param_name, val, expected_type)
        except TypeError as e:
            if print_on_error:
                traceback.print_exc()
            return False
        return True


class AT(TypedDict):
    a: str

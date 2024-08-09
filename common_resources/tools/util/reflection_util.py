import builtins
import importlib
import traceback
import typing
from enum import Enum
from typing import Any, Dict, List, Optional, Type

from typeguard import check_type
from typeguard._exceptions import TypeCheckError

from common_resources.tools.constants.symbol_constants import PERIOD, UNDERSCORE, EMPTY_STRING
from common_resources.tools.t_logging.logger_manager import logger
from common_resources.tools.util.param_specs import ParamSpecs
from common_resources.tools.util.str_util import StrUtil
from common_resources.tools.variables.undetermined_variable import UndeterminedVariable


class ParamScope(Enum):
    PUBLIC = 0
    PROTECTED = 1
    PRIVATE = 2


class ReflectionUtil:

    @staticmethod
    def has_constructor_param(class_type: Type, param: str) -> bool:
        """
        Checks whether param of given name is accepted in type constructor.
        :param class_type: The class type whose constructor is checked.
        :param param: The param name to check for.
        :return: True if constructor accepts param of given name.
        """
        constructor_param_names = ParamSpecs.create_from_method(class_type.__init__).param_names
        return param in constructor_param_names

    @staticmethod
    def get_constructor_params(class_type: Type, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Checks whether param of given name is accepted in type constructor.
        :param class_type: The class type whose constructor is checked.
        :param params: The param names to check for.
        :return: All params that would be in the constructor.
        """
        param_specs = ParamSpecs.create_from_method(class_type.__init__)
        return param_specs.extract_params_from_kwargs(**params)

    @staticmethod
    def get_target_class_from_type(target_class: Type) -> Type:
        """
        Gets the target class from the given type (i.e. if Union[someclass] will return someclass
        :param target_class: the type
        :return: the target class
        """
        if typing.get_origin(target_class) is typing.Union:
            return typing.get_args(target_class)[0]
        return target_class

    @staticmethod
    def is_instance_or_subclass(target_class: Type, source_class: Type, reversible: bool = False) -> bool:
        """
        Returns whether target is instance of sub-class of source class.
        :param target_class: The class being tested for containment
        :param source_class: The containment class.
        :param reversible: If True, either class may be a subclass of the either.
        :return: Boolean representing if target is contained within source.
        """
        try:
            res = isinstance(target_class, source_class) or issubclass(target_class, source_class)
            if reversible:
                res = res or issubclass(source_class, target_class)
            return res
        except Exception:
            return False

    @staticmethod
    def copy_fields(source: Dict, include: List[str] = None, exclude: List[str] = None) -> Dict[str, Any]:
        """
        Creates a copy of the source fields
        :param source: the source fields
        :param include: copies only those in include list if given
        :param exclude: copies all but those in exclude list if given
        :return: a copy of the fields
        """
        if include:
            return {field: source[field] for field in include}
        elif exclude:
            return {field: source[field] for field in source.keys() if field not in exclude}
        else:
            raise ValueError("Specify fields to include or exclude.")

    @staticmethod
    def get_field_scope(field_name: str, class_name: str = None) -> ParamScope:
        """
        Calculates the scope of the field through scope naming convention.
        :param field_name: The name of the field in instance.
        :param class_name: The name of the class. Used for detecting private fields.
        :return: Param
        """
        class_prefix = None
        if class_name:
            if class_name.startswith(UNDERSCORE):
                raise ValueError("Expected class name to not start with underscore: " + class_name)
            class_prefix = "_%s" % class_name
        prefix = field_name[:2]
        if "__" == prefix:
            return ParamScope.PRIVATE
        elif UNDERSCORE == prefix[:1]:
            if class_prefix and field_name.startswith(class_prefix):
                return ReflectionUtil.get_field_scope(field_name.replace(class_prefix, ""))
            return ParamScope.PROTECTED
        return ParamScope.PUBLIC

    @staticmethod
    def get_fields(instance: Any, scope: ParamScope = ParamScope.PUBLIC, ignore: List[str] = None) -> Dict:
        """
        Returns the fields of the instance within the scope given.
        :param ignore: will ignore any fields in this list
        :param instance: The instance whose fields are returned.
        :param scope: The scope of the fields to return.
        :return: Dictionary whose keys are field names and values are field values.
        """
        if hasattr(instance, "_fields"):  # named tuple
            return {field: getattr(instance, field) for field in instance._fields}

        params = {}

        for param_id in vars(instance):
            if ignore and param_id in ignore:
                continue
            param_scope = ReflectionUtil.get_field_scope(param_id, class_name=instance.__class__.__name__)
            if param_scope.value <= scope.value:
                param_value = getattr(instance, param_id)
                params[param_id] = param_value
        return params

    @staticmethod
    def get_enum_key(enum: Type[Enum], instance) -> str:
        """
        Returns the key in enum whose value is the class of instance.
        :param enum: Enum containing classes are values.
        :param instance: The instance whose class is returned.
        :return: Enum key whose value is the class of the instance.
        """
        for enum_key in enum:
            if isinstance(instance, enum_key.value):
                return enum_key.name
        raise ValueError("Could not convert " + str(type(instance)) + " into" + str(enum) + PERIOD)

    @staticmethod
    def set_attributes(instance: Any, params: Dict, missing_ok=False) -> Any:
        """
        Sets the instance variables matching param keys to param values.
        :param instance: The object whose properties will be updated.
        :param params: Dictionary whose keys match field names and values are set to field.
        :param missing_ok: Whether missing properties should be ignored.
        :return: Updated instance.
        """
        for param_name, param_value in params.items():
            if hasattr(instance, param_name):
                setattr(instance, param_name, param_value)
            elif not missing_ok:
                raise ValueError(f"Instance {instance} missing property {param_name}.")
        return instance

    @staticmethod
    def copy_attributes(instance: Any, other: Any, param_scope: ParamScope = ParamScope.PUBLIC, fields: List[str] = None) -> None:
        """
        Copies attributes in instance to the other.
        :param instance: The instance whose values are moved to the other.
        :param other: The object whose values are getting set.
        :param param_scope: The scope of the attributes to copy over. Defaults to public
        :param fields: The fields to copy over.
        :return: None
        """
        values = ReflectionUtil.get_fields(instance, param_scope)
        if fields:
            values = {field: field_value for field, field_value in values.items() if field in fields}
        ReflectionUtil.set_attributes(other, values)

    @staticmethod
    def get_typed_class(typed_obj: Any) -> typing.Tuple[str, List[Type]]:
        """
        Returns the base class and the child class.
        e.g.
        Dict[KeyClass, ParentClass] -> Dict, KeyClass, ParentClass
        List[Class] -> List, Class
        Optional[Class] -> Class
        :param typed_obj:
        :return:
        """
        if not ReflectionUtil.is_typed_class(typed_obj):
            raise ValueError("Expected class to be Typed class.")

        origin = typing.get_origin(typed_obj)
        type_args = ReflectionUtil.get_arg_types(typed_obj)
        if origin is typing.Union:
            return "union", *type_args
        elif origin is list:
            if not type_args:
                type_args = [None]
            assert len(type_args) == 1, f"Found multiple typed for list: {type_args}"
            return "list", type_args[0]
        elif isinstance(origin, typing.Callable):
            return "callable", *type_args
        else:
            raise ValueError("Unable ")

    @staticmethod
    def is_function(unknown_obj) -> bool:
        """
        Returns true if the object is a function else false
        :param unknown_obj: The obj to test if its a function
        :return: True if it is a function else False
        """
        return type(unknown_obj).__name__ in ["function", "builtin_function_or_method", "method", "classmethod",
                                              "staticmethod", "abstractmethod"]

    @staticmethod
    def is_typed_class(class_obj: Type):
        """
        Returns whether the class is a typed class. (Optional, List, Dict, Tuple, ect.)
        :param class_obj: Class to be determined.
        :return: True is class is typed, false otherwise.
        """
        return hasattr(class_obj, "_name")  # TODO: Come up with better hueristc

    @staticmethod
    def get_arg_types(class_obj: Type):
        """
        Returns the typed arguments to class.
        :param class_obj:
        :return:
        """
        assert ReflectionUtil.is_typed_class(class_obj), f"{class_obj} is not a typed class."
        if not hasattr(class_obj, "__args__"):
            return []
        type_args = class_obj.__args__
        return type_args

    @staticmethod
    def is_none_type(class_obj):
        """
        Heuristically determines if class is none type. This class is unimportable in python.
        :param class_obj: The class to be determined.
        :return: True is none type.
        """
        return hasattr(class_obj, "__name__") and class_obj.__name__ == "NoneType"

    @staticmethod
    def is_union(class_obj: Any):
        """
        :param class_obj: The class to check.
        :return: Returns whether class is an optional type.
        """
        return typing.get_origin(class_obj) is typing.Union

    @staticmethod
    def is_typed_dict(expected_type: Type):
        """
        :param expected_type:
        :return: Returns true if expected type is a typed dictionary, false otherwise.
        """
        return hasattr(expected_type, "__annotations__") and \
            len(getattr(expected_type, "__annotations__")) > 0 and \
            issubclass(expected_type, dict)

    @staticmethod
    def get_cls_from_path(class_path: str) -> Optional[Type]:
        """
        Gets the class type from a relative path to the class if it exists, else returns None
        :param class_path: The path to the class in the following format tgen.modulePath.className
        :return: The class or None if it does not exist
        """
        try:
            spit_path = class_path.split(PERIOD)
            module_path, class_name = PERIOD.join(spit_path[:-1]), spit_path[-1]
            module = builtins if "builtins" in class_path else importlib.import_module(module_path)
            if not hasattr(module, class_name):
                outer_class_name = StrUtil.snake_case_to_pascal_case(spit_path[-2])
                module = getattr(module, outer_class_name)
            return getattr(module, class_name)
        except (ImportError, AttributeError):
            return

    @staticmethod
    def extract_name_of_variable(var_as_string: str, is_self_property: bool = False, class_attr: Any = None,
                                 nested_var: str = None) -> str:
        """
        After calling f"{var=}" on object, this method will extract the actual variable name
        :param var_as_string: Call f"{var=}" on object and pass it in
        :param is_self_property: If True,the variable is a property of self
        :param class_attr: If given, variable is an attribute of the class
        :param nested_var: If given, variable is nested inside another variable in the main class
        :return: The name of the variable as a string
        """
        var_name = var_as_string.split('=')[0]
        if is_self_property:
            var_name = var_name.split("self.")[-1]
        elif class_attr:
            var_name = var_name.split(f"{class_attr.__name__}.")[-1]
        if nested_var:
            var_name = var_name.split(f"{nested_var}.")[-1]
        if var_name.startswith("__") and class_attr:
            var_name = f"_{class_attr.__name__}{var_name}"
        return var_name

    @staticmethod
    def is_type(val: Any, expected_type: typing.Union[Type], param_name: str = EMPTY_STRING, print_on_error: bool = True,
                reversible: bool = False) -> bool:
        """
        Checks if the value is of the expected type for the variable with the given name
        :param val: the value
        :param expected_type: expected type or typing generic
        :param param_name: the name of the parameter being tested
        :param print_on_error: Whether to print exception if error occurs.
        :param reversible: If True, either class may be a subclass of the either.
        :return: True if the type of val matches expected_type, False otherwise
        """
        try:
            if isinstance(val, UndeterminedVariable):
                return True

            if ReflectionUtil.is_typed_dict(expected_type):
                if not ReflectionUtil.is_instance_or_subclass(val, dict):
                    raise TypeError(f"Expected a dictionary but while parsing {expected_type} got: {val}")
                for field_name, expected_field_type in expected_type.__annotations__.items():
                    check_type(expected_type=expected_field_type, value=val.get(field_name, None))
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
                    if not ReflectionUtil.is_instance_or_subclass(val, list):
                        return False
                    if child_type is not None:
                        invalid_runs = [v for v in val if not ReflectionUtil.is_type(v, child_type, param_name, print_on_error=False,
                                                                                     reversible=reversible)]
                        if len(invalid_runs) > 0:
                            raise TypeError(f"List elements {invalid_runs} was not of type {child_type}.")
                    return True
                elif parent_class == "union" or parent_class == "optional":
                    queries = [c for c in child_classes if ReflectionUtil.is_type(val, c, param_name, print_on_error=False,
                                                                                  reversible=reversible)]
                    if len(queries) == 0:
                        raise TypeError(f"{val} was not of type: {child_classes}")
                    return True
                elif parent_class == "callable":
                    check_type(expected_type=expected_type, value=val)
                    return True
                else:
                    expected_type = parent_class
            try:
                is_instance = ReflectionUtil.is_instance_or_subclass(val, expected_type, reversible=reversible)
                if is_instance:
                    return True
            except Exception:
                pass
            check_type(expected_type=expected_type, value=val)
        except (TypeCheckError, TypeError) as e:
            if print_on_error:
                logger.exception(f"{param_name} type check failed")
            return False
        return True

    @staticmethod
    def get_base_class_type(type_: Type) -> Type:
        """
        Gets the main class type (for example if Optional[SomeType] then SomeType will be returned).
        :param type_: The typed class.
        :return: The main class type (for example if Optional[SomeType] then SomeType will be returned).
        """
        if ReflectionUtil.is_typed_class(type_):
            expected_type_name = type_._name
            if expected_type_name == "Any":
                return Any

            parent_class, *child_classes = ReflectionUtil.get_typed_class(type_)
            if parent_class in {"dict", "list", "union", "optional"}:
                return child_classes[0]
            elif parent_class == "callable":
                return typing.Callable
            else:
                return parent_class
        return type_

    @staticmethod
    def is_primitive(obj: Any) -> bool:
        """
        Checks if object is of type int, float, str or bool.
        :param obj: The object to check if instance of primitive.
        :return: True if obj is instance of primitive, false otherwise.
        """
        primitive_type_classes = [str, int, float, bool]
        return any([isinstance(obj, t) for t in primitive_type_classes])

    @staticmethod
    def get_class_name(obj: Any) -> str:
        """
        Returns the name of the class, separated by spaces
        :param obj: The object to get the name of
        :return: The name of the class, separated by spaces
        """
        from common_resources.data.processing.cleaning.separate_camel_case_step import SeparateCamelCaseStep
        cls = obj.__class__ if not isinstance(obj, type) else obj
        return SeparateCamelCaseStep().run([cls.__name__])[0]

    @staticmethod
    def get_obj_full_path(obj: Any) -> str:
        """
        Gets the full path of an obj including its module path and subsequent qual name (e.g. for a function: module.Class.function).
        :param obj: The obj to get the path from.
        :return: Full path of an obj (e.g. for a function: module.Class.function).
        """
        module_path = obj.__module__
        qual_name = obj.__qualname__
        return PERIOD.join([module_path, qual_name])

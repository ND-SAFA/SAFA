import typing
from enum import Enum
from typing import Any, Dict, List, Type

from tgen.constants.deliminator_constants import PERIOD, UNDERSCORE


class ParamScope(Enum):
    PUBLIC = 0
    PROTECTED = 1
    PRIVATE = 2


class ReflectionUtil:

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
    def is_instance_or_subclass(target_class: Type, source_class: Type) -> bool:
        """
        Returns whether target is instance of sub-class of source class.
        :param target_class: The class being tested for containment
        :param source_class: The containment class.
        :return: Boolean representing if target is contained within source.
        """
        try:
            return isinstance(target_class, source_class) or issubclass(target_class, source_class)
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
    def copy_attributes(instance: Any, other: Any, param_scope: ParamScope = ParamScope.PUBLIC) -> None:
        """
        Copies attributes in instance to the other.
        :param instance: The instance whose values are moved to the other.
        :param other: The object whose values are getting set.
        :param param_scope: The scope of the attributes to copy over. Defaults to public
        :return: None
        """
        values = ReflectionUtil.get_fields(instance, param_scope)
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
        elif isinstance(origin, list):
            assert len(type_args) == 1, f"Found multiple typed for list: {type_args}"
            return "list", type_args[0]
        elif isinstance(origin, typing.Callable):
            return "callable", *type_args
        else:
            raise ValueError("Unable ")

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
        return hasattr(expected_type, "__annotations__") and issubclass(expected_type, dict)

from enum import Enum
from typing import Any, Dict, List, Type


class ParamScope(Enum):
    LOCAL = 0
    PROTECTED = 1
    PRIVATE = 2


class ReflectionUtil:

    @staticmethod
    def copy_fields(source: Dict, fields: List[str]):
        return {field: source[field] for field in fields}

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
            if class_name.startswith("_"):
                raise ValueError("Expected class name to not start with underscore: " + class_name)
            class_prefix = "_%s" % class_name
        prefix = field_name[:2]
        if "__" == prefix:
            return ParamScope.PRIVATE
        elif "_" == prefix[:1]:
            if class_prefix and field_name.startswith(class_prefix):
                return ReflectionUtil.get_field_scope(field_name.replace(class_prefix, ""))
            return ParamScope.PROTECTED
        return ParamScope.LOCAL

    @staticmethod
    def get_fields(instance: Any, scope: ParamScope) -> Dict:
        """
        Returns the fields of the instance within the scope given.
        :param instance: The instance whose fields are returned.
        :param scope: The scope of the fields to return.
        :return: Dictionary whose keys are field names and values are field values.
        """
        params = {}
        for param_id in vars(instance):
            param_name = param_id
            param_scope = ReflectionUtil.get_field_scope(param_name, class_name=instance.__class__.__name__)
            if param_scope.value <= scope.value:
                param_value = getattr(instance, param_id)
                params[param_name] = param_value
        return params

    @staticmethod
    def get_enum_key(enum: Type[Enum], instance):
        """
        Returns the key in enum whose value is the class of instance.
        :param enum: Enum containing classes are values.
        :param instance: The instance whose class is returned.
        :return: Enum key whose value is the class of the instance.
        """
        for enum_key in enum:
            if isinstance(instance, enum_key.value):
                return enum_key.name
        raise ValueError("Could not convert " + str(type(instance)) + " into SupportedDatasetCreator.")

    @staticmethod
    def set_attributes(instance: Any, params: Dict):
        """
        Sets the instance variables matching param keys to param values.
        :param instance: The object whose properties will be updated.
        :param params: Dictionary whose keys match field names and values are set to field.
        :return: Updated instance.
        """
        for param_name, param_value in params.items():
            setattr(instance, param_name, param_value)
        return instance

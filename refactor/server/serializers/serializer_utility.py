from typing import Dict, OrderedDict

from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class SerializerUtility:
    @staticmethod
    def update_error():
        raise NotImplementedError("Update has not implemented for serializers. Please create new serialier.")

    @staticmethod
    def has_unknown_fields(instance: serializers.Serializer, initial_data: Dict, fields: OrderedDict):
        if hasattr(instance, 'initial_data'):
            unknown_keys = set(initial_data.keys()) - set(fields.keys())
            if unknown_keys:
                raise ValidationError("Got unknown fields: {}".format(unknown_keys))

    @staticmethod
    def create_children_serializers(validated_data: Dict, fields: OrderedDict) -> Dict:
        """
        Creates each field in serializer of type serializer.
        :param validated_data: The validated request data.
        :param fields: The fields of the serializer.
        :return: Dictionary containing created field values.
        """
        kwargs = {}
        for field in fields.values():
            field_name = field.source
            if field_name not in validated_data:
                continue
            is_serializer = isinstance(field, serializers.Serializer)
            has_child_serializer = hasattr(field, "child") and isinstance(field.child, serializers.Serializer)
            if is_serializer or has_child_serializer:
                kwargs[field_name] = field.create(validated_data[field_name])
            else:
                kwargs[field_name] = validated_data[field_name]
        return kwargs

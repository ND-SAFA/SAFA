from typing import Dict

from rest_framework import serializers


class AbstractSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        raise NotImplementedError()

    def create(self, validated_data: Dict):
        kwargs = {}
        fields = self.fields.fields
        for field in fields.values():
            field_name = field.source
            is_serializer = isinstance(field, serializers.Serializer)
            has_child_serializer = hasattr(field, "child") and isinstance(field.child, serializers.Serializer)
            if is_serializer or has_child_serializer:
                kwargs[field_name] = field.create(validated_data[field_name])
            else:
                kwargs[field_name] = validated_data[field_name]
        return kwargs

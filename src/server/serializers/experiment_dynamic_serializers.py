import json
import os
from typing import Any, Dict, Type, TypeVar, get_type_hints

from django.core.wsgi import get_wsgi_application
from rest_framework import serializers

from server.serializers.serializer_utility import SerializerUtility
from train.trainer_args import TrainerArgs
from util.reflection_util import ParamScope, ReflectionUtil

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')

application = get_wsgi_application()

ClassType = TypeVar("ClassType")


class DynamicSerializer(serializers.Serializer):

    def __init__(self, instance_class: Type[ClassType], **kwargs):
        super().__init__(**kwargs)
        self.instance_class = instance_class
        self.field2type: Dict[str, Any] = get_type_hints(instance_class)
        self.field2value: Dict[str, Any] = ReflectionUtil.get_fields(instance_class, ParamScope.LOCAL)

        print(self.field2value)
        for instance_field in self.field2value:
            if instance_field not in self.field2type:
                class_name = self.instance_class.__name__
                message = "%s does not have type hint for field (%s)." % (class_name, instance_field)
                raise ValueError(message)

        for instance_field_name in ReflectionUtil.get_fields(instance_class, ParamScope.LOCAL):
            field_type_class = self.field2type[instance_field_name]
            serializer_field_name = SerializerUtility.to_camel_case(instance_field_name)
            kwargs = {"required": True}
            if instance_field_name != serializer_field_name:
                kwargs["source"] = instance_field_name
            self.fields[serializer_field_name] = create_field_type(field_type_class, **kwargs)

    def update(self, instance, validated_data):
        raise NotImplementedError("Under construction.")

    def create(self, validated_data: Dict) -> ClassType:
        return self.instance_class(**validated_data)


def create_field_type(field_type: Type[object], **kwargs):
    print(field_type, type(field_type))
    if ReflectionUtil.is_instance_or_subclass(field_type, str):
        return serializers.CharField(max_length=200, **kwargs)
    if ReflectionUtil.is_instance_or_subclass(field_type, int):
        return serializers.IntegerField(**kwargs)
    if ReflectionUtil.is_instance_or_subclass(field_type, bool):
        return serializers.BooleanField(**kwargs)
    else:
        return serializers.CharField(many=True, **kwargs)
    raise Exception("Unknown field type:" + field_type.__name__)


if __name__ == "__main__":
    payload = {
        "max_seq_length": 255
    }
    serializer = DynamicSerializer(TrainerArgs, data=payload)
    assert serializer.is_valid(), json.dumps(serializer.errors, indent=4)
    instance = serializer.save()
    print(instance)

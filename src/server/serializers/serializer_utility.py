from typing import Dict, OrderedDict

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from tracer.datasets.trainer_datasets_container import TrainerDatasetsContainer


class SerializerUtility:
    @staticmethod
    def create_trainer_dataset_container(kwargs: Dict, container_param: str, dataset_param: str = "data",
                                         export_param: str = "trainer_dataset_container"):
        """
        Reads dataset from kwargs and wraps it in a trainer dataset container.
        :param kwargs: The kwargs to extract dataset from.
        :param container_param: The name of parameter in the dataset container to store dataset under.
        :param dataset_param: The name of the parameter in kwargs containing dataset.
        :param export_param: The name of the parameter to export trainer dataset container to in kwargs.
        :return: None
        """
        dataset = kwargs.pop(dataset_param).create()
        container_kwargs = {container_param: dataset}
        trainer_datasets_container = TrainerDatasetsContainer(**container_kwargs)
        kwargs[export_param] = trainer_datasets_container

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

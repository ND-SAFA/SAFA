from typing import Dict

from rest_framework import serializers

from jobs.job_factory import JobFactory
from server.serializers.dataset.dataset_creator_serializer import DatasetCreatorSerializer
from server.serializers.serializer_utility import SerializerUtility
from server.serializers.tests.base_serializer_test import BaseSerializerTest
from tracer.util.reflection_util import ParamScope, ReflectionUtil


class JobFactorySerializer(serializers.Serializer):
    """
    Provides generic serialization and deserialization of JobFactory
    """

    def validate(self, attrs):
        """
        Checks that data is valid and that no extra fields have been included.
        :param attrs: The incoming data.
        :return: The validated data.
        """
        data = super().validate(attrs)
        SerializerUtility.has_unknown_fields(self, self.initial_data, self.fields.fields)
        return data

    def create(self, validated_data: Dict) -> JobFactory:
        """
        Creates AppEntity from validated data.
        :param validated_data: Map of property names to values.
        :return: Instance of AppEntity with validated data as kwargs
        """
        kwargs = SerializerUtility.create_children_serializers(validated_data, self.fields.fields)
        return JobFactory(**kwargs)

    def update(self, instance: JobFactory, validated_data: Dict):
        SerializerUtility.update_error()

    def save(self, **kwargs) -> JobFactory:
        """
        Typed wrapper for save method.
        :param kwargs:
        :return:
        """
        return super().save(**kwargs)

    def to_representation(self, instance: JobFactory):
        data = {
            "settings": instance.additional_job_params
        }
        ignore_vars = ["additional_job_params"]
        fields = ReflectionUtil.get_fields(instance, ParamScope.LOCAL, ignore=ignore_vars)
        fields = {BaseSerializerTest.to_camel_case(k): v for k, v in fields.items()}
        data.update(fields)
        dataset_container = instance.trainer_dataset_container
        dataset = None
        if dataset_container.train_dataset:
            dataset = dataset_container.train_dataset
        if dataset_container.eval_dataset:
            dataset = dataset_container.eval_dataset
        if dataset is None:
            raise ValueError("Dataset not defined.")
        dataset_representation = DatasetCreatorSerializer().to_representation(dataset)
        data["data"] = dataset_representation
        return data

from typing import Dict

from rest_framework import serializers

from jobs.job_factory import JobFactory
from server.serializers.job_factory.job_factory_converter import JobFactoryConverter
from server.serializers.serializer_utility import SerializerUtility


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
        SerializerUtility.assert_no_unknown_fields(self.initial_data, self.fields.fields)
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

    def to_representation(self, instance: JobFactory) -> Dict:
        """
        Exports job factory into API format.
        :param instance: The job factory to convert.
        :return: JSON data representing job factory.
        """
        return JobFactoryConverter.job_factory_representation(instance)

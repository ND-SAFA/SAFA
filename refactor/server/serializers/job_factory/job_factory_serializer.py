from typing import Dict

from rest_framework import serializers

from jobs.job_factory import JobFactory


class JobFactorySerializer(serializers.Serializer):
    """
    Provides generic serialization and deserialization of JobFactory
    """

    def create(self, validated_data: Dict) -> JobFactory:
        """
        Creates AppEntity from validated data.
        :param validated_data: Map of property names to values.
        :return: Instance of AppEntity with validated data as kwargs
        """
        return JobFactory(**validated_data)

    def update(self, instance: JobFactory, validated_data: Dict) -> JobFactory:
        """
        Updates instance with property defined in validated data.
        :param instance: The app entity to update.
        :param validated_data: The values to update the entity with
        :return: AppEntity with updated values
        """
        instance.set_args(**validated_data)
        return instance

    def save(self, **kwargs) -> JobFactory:
        """
        Typed wrapper for save method.
        :param kwargs:
        :return:
        """
        return super().save(**kwargs)

from abc import abstractmethod
from dataclasses import dataclass
from typing import Dict, Generic, Type, TypeVar

from rest_framework import serializers

from tracer.models.base_models.supported_base_model import SupportedBaseModel


@dataclass
class ModelIdentifier:
    base_model: SupportedBaseModel
    model_path: str
    output_dir: str


"""
The entity to be returned by base serializer
"""
AppEntity = TypeVar('AppEntity')


class BaseSerializer(serializers.Serializer, Generic[AppEntity]):
    """
    Provides generic
    """

    def create(self, validated_data: Dict) -> AppEntity:
        """
        Creates AppEntity from validated data.
        :param validated_data: Map of property names to values.
        :return: Instance of AppEntity with validated data as kwargs
        """
        app_entity_class = self.get_app_entity_class()
        return app_entity_class(**validated_data)

    def update(self, instance: AppEntity, validated_data: Dict) -> AppEntity:
        """
        Updates instance with property defined in validated data.
        :param instance: The app entity to update.
        :param validated_data: The values to update the entity with
        :return: AppEntity with updated values
        """
        for property_name, property_value in validated_data.items():
            setattr(instance, property_name, property_value)
        return instance

    def save(self, **kwargs) -> AppEntity:
        """
        Typed wrapper for save method.
        :param kwargs:
        :return:
        """
        return super().save(**kwargs)

    @abstractmethod
    def get_app_entity_class(self) -> Type[AppEntity]:
        """
        Returns the AppEntity class returned when serializing.
        :return: Class of AppEntity
        """
        pass

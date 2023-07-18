from typing import Dict, Generic, TypeVar

from rest_framework import serializers

PayloadType = TypeVar("PayloadType")


class AbstractSerializer(serializers.Serializer, Generic[PayloadType]):
    """
    Abstract class for all serializeres.
    """

    def update(self, instance, validated_data):
        raise NotImplementedError(f"Update is not implemented on {self.__class__.__name__}.")

    def create(self, validated_data: Dict):
        return validated_data

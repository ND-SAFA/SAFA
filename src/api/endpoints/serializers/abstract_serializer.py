from typing import Dict, Generic, TypeVar

from rest_framework import serializers

PayloadType = TypeVar("PayloadType")


class AbstractSerializer(serializers.Serializer, Generic[PayloadType]):
    """
    Abstract class for all serializeres.
    """

    def update(self, instance, validated_data):
        """
        Deprecated.
        :param instance: The instance to update.
        :param validated_data: Thew new instance data.
        :return: Throws not implemented error.
        """
        raise NotImplementedError(f"Update is not implemented on {self.__class__.__name__}.")

    def create(self, validated_data: Dict):
        """
        Serializes input object from request data.
        :param validated_data: Request data in JSON.
        :return: The serialized data.
        """
        return validated_data

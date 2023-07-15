from typing import Dict, Generic, TypeVar

from rest_framework import serializers

PayloadType = TypeVar("PayloadType")


class AbstractSerializer(serializers.Serializer, Generic[PayloadType]):
    """
    Abstract class for all serializeres.
    """

    def create(self, validated_data: Dict):
        return validated_data

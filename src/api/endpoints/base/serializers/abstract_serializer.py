from typing import Generic, TypeVar

from rest_framework import serializers

PayloadType = TypeVar("PayloadType")


class AbstractSerializer(serializers.Serializer, Generic[PayloadType]):
    """
    Abstract class for all serializeres.
    """
 
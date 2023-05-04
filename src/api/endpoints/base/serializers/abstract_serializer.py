from rest_framework import serializers

from api.utils.serializer_utility import SerializerUtility


class AbstractSerializer(serializers.Serializer):
    """
    Abstract class for all serializeres.
    """

    def update(self, instance, validated_data):
        """
        Not implemented. Throws error if called.
        """
        SerializerUtility.update_error()

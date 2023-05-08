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

    def create(self, validated_data):
        """
        Recursively creates child data. Under construction, currently non-functional.
        :param validated_data: The data created.
        :return: The validated data.
        """
        data = SerializerUtility.create_children_serializers(validated_data, self.fields.fields)
        return data

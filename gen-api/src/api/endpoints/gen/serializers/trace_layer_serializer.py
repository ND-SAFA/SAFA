from rest_framework import serializers

from api.endpoints.gen.serializers.abstract_serializer import AbstractSerializer
from api.utils.serializer_utility import SerializerUtility
from tgen.common.objects.trace_layer import TraceLayer


class LayerSerializer(AbstractSerializer):
    parent = serializers.CharField(help_text="The parent type.", allow_blank=False, allow_null=False, required=True)
    child = serializers.CharField(help_text="The child type.", allow_blank=False, allow_null=False, required=True)

    def update(self, **kwargs):
        """
        Throws error, not implemented.
        :param kwargs: Ignored parameters.
        :return: None, error is thrown.
        """
        SerializerUtility.update_error()

    def create(self, validated_data) -> TraceLayer:
        """
        Serializes the input data for a layer to trace between.
        :param validated_data: The validated request data.
        :return: The trace layer instance.
        """
        trace_layer = TraceLayer(parent=validated_data["parent"], child=validated_data["child"])
        return trace_layer

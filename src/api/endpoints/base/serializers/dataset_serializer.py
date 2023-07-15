from typing import Dict, List, TypedDict

from rest_framework import serializers

from api.endpoints.base.serializers.abstract_serializer import AbstractSerializer
from api.utils.serializer_utility import SerializerUtility
from tgen.data.readers.definitions.api_definition import ApiDefinition
from tgen.ranking.common.trace_layer import TraceLayer


class DatasetPayload(TypedDict):
    """
    Type of payload for a dataset
    """
    artifact_layers: Dict[str, Dict[str, str]]
    layers: List[TraceLayer]


class TraceLayerSerializer(AbstractSerializer):
    parent = serializers.CharField(help_text="The parent type.", allow_blank=False, allow_null=False, required=True)
    child = serializers.CharField(help_text="The child type.", allow_blank=False, allow_null=False, required=True)

    def update(self, **kwargs):
        """
        Throws error, not implemented.
        :param kwargs: Ignored parameters.
        :return: None, error is thrown.
        """
        SerializerUtility.update_error()

    def create(self, validated_data):
        trace_layer = TraceLayer(parent=validated_data["parent"], child=validated_data["child"])
        return trace_layer


class DatasetSerializer(AbstractSerializer):
    """
    Serializes datasets for trace link prediction.
    """
    artifact_layers = serializers.DictField(
        child=serializers.DictField(
            child=serializers.CharField(help_text="a"),
            help_text="a"
        ),
        help_text="a"
    )
    layers = TraceLayerSerializer(many=True, help_text="The layers being traced.")

    def create(self, validated_data) -> ApiDefinition:
        """
        Validates dataset payload.
        :param validated_data: The data validated by django.
        :return:
        """
        layer_serializer = TraceLayerSerializer(many=True, data=validated_data["layers"])
        layer_serializer.is_valid(raise_exception=True)
        layers = layer_serializer.save()
        return ApiDefinition(artifact_layers=validated_data["artifact_layers"],
                             layers=layers,
                             true_links=[])

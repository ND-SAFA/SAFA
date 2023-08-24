from typing import Dict, List, TypedDict

from rest_framework import serializers

from api.constants.api_constants import LONG_TEXT
from api.endpoints.serializers.abstract_serializer import AbstractSerializer
from api.endpoints.serializers.artifact_serializer import ArtifactSerializer
from api.endpoints.serializers.trace_layer_serializer import TraceLayerSerializer
from tgen.data.readers.definitions.api_definition import ApiDefinition
from tgen.ranking.common.trace_layer import TraceLayer


class DatasetPayload(TypedDict):
    """
    Type of payload for a dataset
    """
    artifact_layers: Dict[str, Dict[str, str]]
    layers: List[TraceLayer]


class DatasetSerializer(AbstractSerializer):
    """
    Serializes datasets for trace link prediction.
    TODO: Create
    """
    artifacts = ArtifactSerializer(many=True, help_text="The artifacts to trace.")
    layers = TraceLayerSerializer(many=True, help_text="The layers being traced.")
    summary = serializers.CharField(max_length=LONG_TEXT, help_text="Pre-generated project summary.", required=False,
                                    allow_null=True,
                                    allow_blank=False)

    def create(self, validated_data) -> ApiDefinition:
        """
        Validates dataset payload.
        :param validated_data: The data validated by django.
        :return:
        """
        layer_serializer = TraceLayerSerializer(many=True, data=validated_data["layers"])
        layer_serializer.is_valid(raise_exception=True)
        layers = layer_serializer.save()
        artifact_serializer = ArtifactSerializer(many=True, data=validated_data["artifacts"])
        artifact_serializer.is_valid(raise_exception=True)
        artifacts = artifact_serializer.save()
        summary = validated_data.get("summary")
        return ApiDefinition(artifacts=artifacts,
                             layers=layers,
                             links=[],
                             summary=summary)

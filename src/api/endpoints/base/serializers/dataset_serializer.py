from typing import Dict, List, TypedDict

from rest_framework import serializers

from api.constants.api_constants import MEDIUM_LENGTH, TEXT_LENGTH
from api.endpoints.base.serializers.abstract_serializer import AbstractSerializer
from api.utils.serializer_utility import SerializerUtility
from tgen.common.util.dataframe_util import DataFrameUtil
from tgen.common.util.enum_util import EnumDict
from tgen.data.dataframes.artifact_dataframe import ArtifactKeys
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


class ArtifactSerializer(AbstractSerializer):
    id = serializers.CharField(help_text="The identifier of the artifact.", required=True)
    content = serializers.CharField(help_text="The body of the artifact", max_length=TEXT_LENGTH, required=True)
    layer_id = serializers.CharField(help_text="The layer this artifact is associated with.", max_length=MEDIUM_LENGTH, required=True)
    name = serializers.CharField(help_text="The human readable name of the artifact.", required=False)
    summary = serializers.CharField(help_text="The summary of the artifact", max_length=TEXT_LENGTH, required=False, allow_null=True,
                                    allow_blank=True)

    def create(self, validated_data: Dict):
        summary = DataFrameUtil.get_optional_value(validated_data, "summary", allow_empty=False)
        return EnumDict({
            ArtifactKeys.ID: validated_data["id"],
            ArtifactKeys.CONTENT: validated_data["content"],
            ArtifactKeys.LAYER_ID: validated_data["layer_id"],
            ArtifactKeys.SUMMARY: summary
        })


class DatasetSerializer(AbstractSerializer):
    """
    Serializes datasets for trace link prediction.
    TODO: Create
    """
    artifacts = ArtifactSerializer(many=True, help_text="The artifacts to trace.")
    layers = TraceLayerSerializer(many=True, help_text="The layers being traced.")
    summary = serializers.CharField(max_length=TEXT_LENGTH, help_text="Pre-generated project summary.", required=False,
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
                             true_links=[],
                             summary=summary)

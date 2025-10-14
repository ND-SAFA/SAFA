from dataclasses import dataclass
from typing import List

from rest_framework import serializers

from api.constants.api_constants import TEXT_LONG, TEXT_MEDIUM
from api.endpoints.gen.serializers.artifact_serializer import ArtifactSerializer
from tgen.common.objects.artifact import Artifact
from tgen.common.util.base_object import BaseObject
from tgen.common.util.dataframe_util import DataFrameUtil


@dataclass
class HGenRequest(BaseObject):
    artifacts: List[Artifact]
    target_types: List[str]
    summary: str


class HGenSerializer(serializers.Serializer):
    """
    Serializes the request for hierarchy generation
    """

    artifacts = ArtifactSerializer(many=True, help_text="List of source artifacts.")
    targetTypes = serializers.ListSerializer(
        help_text="List of target types to generate.",
        child=serializers.CharField(max_length=TEXT_MEDIUM, help_text="The types of artifacts to generate."))
    summary = serializers.CharField(max_length=TEXT_LONG, help_text="Pre-generated project summary.", required=False,
                                    allow_null=True,
                                    allow_blank=False)

    def create(self, validated_data) -> HGenRequest:
        """
        Serializes HGEN request.
        :param validated_data: The JSON input data.
        :return: HGEN Request.
        """
        artifact_serializer = ArtifactSerializer(data=validated_data["artifacts"], many=True)
        artifact_serializer.is_valid(raise_exception=True)
        artifacts = artifact_serializer.save()
        target_types = validated_data["targetTypes"]
        summary = DataFrameUtil.get_optional_value_from_df(validated_data, "summary", allow_empty=False)
        return HGenRequest(artifacts=artifacts, target_types=target_types, summary=summary)

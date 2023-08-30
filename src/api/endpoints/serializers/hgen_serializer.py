from dataclasses import dataclass
from typing import List

from rest_framework import serializers

from api.constants.api_constants import LONG_TEXT, MEDIUM_TEXT
from api.endpoints.serializers.artifact_serializer import ArtifactSerializer
from tgen.common.artifact import Artifact
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
        child=serializers.CharField(max_length=MEDIUM_TEXT, help_text="The types of artifacts to generate."))
    summary = serializers.CharField(max_length=LONG_TEXT, help_text="Pre-generated project summary.", required=False,
                                    allow_null=True,
                                    allow_blank=False)

    def create(self, validated_data) -> HGenRequest:
        artifact_serializer = ArtifactSerializer(data=validated_data["artifacts"], many=True)
        artifact_serializer.is_valid(raise_exception=True)
        artifacts = artifact_serializer.save()
        target_types = validated_data["targetTypes"]
        summary = DataFrameUtil.get_optional_value_from_df(validated_data, "summary", allow_empty=False)
        return HGenRequest(artifacts=artifacts, target_types=target_types, summary=summary)

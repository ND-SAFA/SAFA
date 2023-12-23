from typing import Dict

from rest_framework import serializers

from api.constants.api_constants import TEXT_LONG, TEXT_MEDIUM
from api.endpoints.serializers.abstract_serializer import AbstractSerializer
from tgen.common.objects.artifact import Artifact
from tgen.common.util.dataframe_util import DataFrameUtil


class ArtifactSerializer(AbstractSerializer):
    id = serializers.CharField(help_text="The identifier of the artifact.", required=True)
    content = serializers.CharField(help_text="The body of the artifact", max_length=TEXT_LONG, required=True, allow_blank=True)
    layer_id = serializers.CharField(help_text="The layer this artifact is associated with.", max_length=TEXT_MEDIUM, required=True)
    name = serializers.CharField(help_text="The human readable name of the artifact.", required=False)
    summary = serializers.CharField(help_text="The summary of the artifact", max_length=TEXT_LONG, required=False, allow_null=True,
                                    allow_blank=True)

    def create(self, validated_data: Dict) -> Artifact:
        summary = DataFrameUtil.get_optional_value_from_df(validated_data, "summary", allow_empty=False)
        return Artifact(id=validated_data["id"],
                        content=validated_data["content"],
                        layer_id=validated_data["layer_id"],
                        summary=summary)

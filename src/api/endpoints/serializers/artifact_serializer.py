from typing import Dict

from rest_framework import serializers

from api.constants.api_constants import LONG_TEXT, MEDIUM_TEXT
from api.endpoints.serializers.abstract_serializer import AbstractSerializer
from tgen.common.util.dataframe_util import DataFrameUtil
from tgen.common.util.enum_util import EnumDict
from tgen.data.dataframes.artifact_dataframe import ArtifactKeys


class ArtifactSerializer(AbstractSerializer):
    id = serializers.CharField(help_text="The identifier of the artifact.", required=True)
    content = serializers.CharField(help_text="The body of the artifact", max_length=LONG_TEXT, required=True)
    layer_id = serializers.CharField(help_text="The layer this artifact is associated with.", max_length=MEDIUM_TEXT, required=True)
    name = serializers.CharField(help_text="The human readable name of the artifact.", required=False)
    summary = serializers.CharField(help_text="The summary of the artifact", max_length=LONG_TEXT, required=False, allow_null=True,
                                    allow_blank=True)

    def create(self, validated_data: Dict):
        summary = DataFrameUtil.get_optional_value(validated_data, "summary", allow_empty=False)
        return EnumDict({
            ArtifactKeys.ID: validated_data["id"],
            ArtifactKeys.CONTENT: validated_data["content"],
            ArtifactKeys.LAYER_ID: validated_data["layer_id"],
            ArtifactKeys.SUMMARY: summary
        })

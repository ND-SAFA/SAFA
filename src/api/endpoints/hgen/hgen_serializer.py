from typing import Dict, List, TypedDict

from rest_framework import serializers

from api.endpoints.summarize.summarize_serializer import SummaryArtifactSerializer


class HGenRequest(TypedDict):
    artifacts: List[Dict]
    targetTypes: List[str]
    summary: str


class HGenSerializer(serializers.Serializer):
    """
    Serializes the request for hierarchy generation
    """

    artifacts = SummaryArtifactSerializer(help_text="List of artifacts to generate parent artifacts from.", many=True)
    targetTypes = serializers.ListSerializer(
        help_text="List of target types to generate.",
        child=serializers.CharField(max_length=1028, help_text="The types of artifacts to generate."))
    summary = serializers.CharField(max_length=100000, help_text="Pre-generated project summary.")

    def create(self, validated_data):
        artifact_serializer = SummaryArtifactSerializer(data=validated_data["artifacts"], many=True)
        artifact_serializer.is_valid(raise_exception=True)
        artifacts = artifact_serializer.save()
        summary = validated_data.get("summary", None)
        target_types = validated_data["targetTypes"]
        return HGenRequest(artifacts=artifacts, targetTypes=target_types, summary=summary)

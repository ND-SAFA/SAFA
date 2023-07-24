from typing import Dict, TypedDict

from rest_framework import serializers

from api.endpoints.base.serializers.abstract_serializer import AbstractSerializer


class ProjectSummaryRequest(TypedDict):
    """
    The request to summarize a project.
    """
    artifacts: Dict[str, str]


class ProjectSummarySerializer(AbstractSerializer):
    artifacts = serializers.DictField(help_text="Artifact map of all the artifacts in the system.",
                                      child=serializers.CharField(help_text="Artifact content."))

    def create(self, validated_data: Dict) -> ProjectSummaryRequest:
        return ProjectSummaryRequest(artifacts=validated_data["artifacts"])

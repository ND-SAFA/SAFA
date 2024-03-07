from typing import Dict, List, TypedDict

from rest_framework import serializers

from api.endpoints.serializers.abstract_serializer import AbstractSerializer
from api.endpoints.serializers.artifact_serializer import ArtifactSerializer
from tgen.common.objects.artifact import Artifact


class ProjectSummaryRequest(TypedDict):
    """
    The request to summarize a project.
    """
    artifacts: List[Artifact]
    kwargs: Dict


class ProjectSummarySerializer(AbstractSerializer):
    artifacts = ArtifactSerializer(many=True, help_text="Artifact map of all the artifacts in the system.")
    kwargs = serializers.DictField(help_text="Additional keyword arguments to project summary job.",
                                   child=serializers.BooleanField(help_text="Flag value."),
                                   required=False, allow_empty=True, allow_null=False)

    def create(self, validated_data: Dict) -> ProjectSummaryRequest:
        """
        Serializes input data into a project summary request.
        :param validated_data: The validated request data.
        :return: Project Summary Request.
        """
        kwargs = validated_data.get("kwargs", {})
        return ProjectSummaryRequest(artifacts=validated_data["artifacts"], kwargs=kwargs)

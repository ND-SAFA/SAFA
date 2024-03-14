from dataclasses import dataclass
from typing import List

from rest_framework import serializers

from api.constants.api_constants import TEXT_LONG
from api.endpoints.gen.serializers.abstract_serializer import AbstractSerializer
from api.endpoints.gen.serializers.artifact_serializer import ArtifactSerializer
from tgen.common.objects.artifact import Artifact


@dataclass
class SummarizeRequest:
    artifacts: List[Artifact]
    project_summary: str


class SummarizeSerializer(AbstractSerializer):
    """
    Serializes the request for artifact summaries.
    """

    artifacts = ArtifactSerializer(many=True, help_text="Artifact information for summarization.")
    projectSummary = serializers.CharField(max_length=TEXT_LONG, help_text="The project summary to include in the summarization.",
                                           required=False, allow_null=True, allow_blank=True)

    def create(self, validated_data) -> SummarizeRequest:
        """
        Serializes input to summary job.
        :param validated_data: The validated data.
        :return: Summarize request.
        """
        summary_serializer = ArtifactSerializer(many=True, data=validated_data["artifacts"])
        summary_serializer.is_valid(raise_exception=True)
        summary_artifacts = summary_serializer.save()
        project_summary = validated_data.get("projectSummary", None)
        project_summary = None if project_summary is None or len(project_summary) == 0 else project_summary
        return SummarizeRequest(artifacts=summary_artifacts, project_summary=project_summary)

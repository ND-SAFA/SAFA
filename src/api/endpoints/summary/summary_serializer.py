from typing import Dict

from rest_framework import serializers

from api.endpoints.base.serializers.abstract_serializer import AbstractSerializer
from api.utils.serializer_utility import SerializerUtility
from tgen.data.chunkers.supported_chunker import SupportedChunker
from tgen.jobs.data_jobs.summarize_artifacts_job import SummaryArtifact


class SummaryArtifactSerializer(serializers.Serializer):
    content = serializers.CharField(max_length=2056)
    type = serializers.ChoiceField(choices=[(e.name, e.value) for e in SupportedChunker])

    def create(self, validated_data):
        return SummaryArtifact(**validated_data)


class SummarySerializer(AbstractSerializer):
    """
    Serializes the request for artifact summaries.
    """

    artifacts = serializers.DictField(child=SummaryArtifactSerializer())
    model = serializers.CharField(max_length=512, required=False)

    def create(self, validated_data: Dict):
        """
        Creates payload
        :param validated_data:
        :return:
        """
        data = SerializerUtility.create_children_serializers(validated_data, self.fields.fields)
        return data

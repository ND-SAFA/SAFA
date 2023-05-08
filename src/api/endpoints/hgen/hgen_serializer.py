from rest_framework import serializers

from api.endpoints.base.serializers.abstract_serializer import AbstractSerializer
from api.endpoints.summary.summary_serializer import SummaryArtifactSerializer


class HGenSerializer(AbstractSerializer):
    """
    Serializes the request for hierarchy generation
    """

    artifacts = serializers.DictField(child=SummaryArtifactSerializer())
    clusters = serializers.ListSerializer(child=serializers.ListSerializer(child=serializers.CharField(max_length=512)))
    model = serializers.CharField(max_length=512, required=False)

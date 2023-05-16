from rest_framework import serializers

from api.endpoints.base.serializers.abstract_serializer import AbstractSerializer
from api.endpoints.summarize.summarize_serializer import SummaryArtifactSerializer


class HGenSerializer(AbstractSerializer):
    """
    Serializes the request for hierarchy generation
    """

    artifacts = serializers.DictField(child=SummaryArtifactSerializer(),
                                      help_text="Artifact map of ID to body.")
    clusters = serializers.ListSerializer(
        child=serializers.ListSerializer(
            child=serializers.CharField(max_length=512, help_text="Artifact ID."),
            help_text="Artifact IDs belonging to cluster."),
        help_text="List of clusters.")
    model = serializers.CharField(max_length=512, required=False, help_text="The model to use for generating artifact.")

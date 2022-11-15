from rest_framework import serializers

from server.serializers.base_serializer import BaseSerializer
from server.serializers.model_identifier_serializer import ModelIdentifierSerializer


class PredictionRequestSerializer(ModelIdentifierSerializer, BaseSerializer):
    sourceLayers = serializers.ListField(child=serializers.DictField(help_text="Map of artifact ids to body."),
                                         help_text="List of source artifact mappings.",
                                         source="source_layers")
    targetLayers = serializers.ListField(child=serializers.DictField(help_text="Map of artifact ids to body."),
                                         help_text="List of target artifact mappings.",
                                         source="target_layers")
    settings = serializers.DictField(help_text="Custom training arguments.")

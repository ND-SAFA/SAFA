from dataclasses import dataclass
from typing import Dict, List

from rest_framework import serializers

from server.serializers.base_serializer import BaseSerializer
from server.serializers.model_identifier_serializer import ModelIdentifier, ModelIdentifierSerializer


@dataclass
class PredictionRequest(ModelIdentifier):
    load_from_storage: bool
    source_layers: List[Dict[str, str]]
    target_layers: List[Dict[str, str]]
    settings: Dict[str, str]


class PredictionRequestSerializer(ModelIdentifierSerializer, BaseSerializer[PredictionRequest]):
    loadFromStorage = serializers.BooleanField(help_text="Whether the model path is in cloud storage.",
                                               source="load_from_storage")
    sourceLayers = serializers.ListField(child=serializers.DictField(help_text="Map of artifact ids to body."),
                                         help_text="List of source artifact mappings.",
                                         source="source_layers")
    targetLayers = serializers.ListField(child=serializers.DictField(help_text="Map of artifact ids to body."),
                                         help_text="List of target artifact mappings.",
                                         source="target_layers")
    settings = serializers.DictField(help_text="Custom training arguments.")

    def get_app_entity_class(self):
        return PredictionRequest

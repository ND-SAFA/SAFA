from dataclasses import dataclass

from rest_enumfield import EnumField
from rest_framework import serializers

from server.serializers.base_serializer import BaseSerializer
from tracer.models.base_models.supported_base_model import SupportedBaseModel


@dataclass
class ModelIdentifier:
    base_model: SupportedBaseModel
    model_path: str
    output_dir: str


class ModelIdentifierSerializer(BaseSerializer[ModelIdentifier]):
    baseModel = EnumField(choices=SupportedBaseModel, help_text="Base model architecture.", source='base_model')
    modelPath = serializers.CharField(max_length=200, help_text="Path to model state.", source="model_path")
    outputDir = serializers.CharField(max_length=200, help_text="Path to store logs and run information.",
                                      source="output_dir")

    def get_app_entity_class(self):
        return ModelIdentifier

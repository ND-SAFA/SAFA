from rest_enumfield import EnumField
from rest_framework import serializers

from config.constants import SAVE_OUTPUT_DEFAULT
from server.serializers.job_factory.job_factory_serializer import JobFactorySerializer
from models.base_models.supported_base_model import SupportedBaseModel


class ModelIdentifierSerializer(JobFactorySerializer):
    """
    Serializer for identifying and loading a model.
    """
    baseModel = EnumField(choices=SupportedBaseModel, help_text="Base model architecture.", source='base_model')
    modelPath = serializers.CharField(max_length=200, help_text="Path to model state.", source="model_path")
    outputDir = serializers.CharField(max_length=200, help_text="Path to store logs and run information.",
                                      source="output_dir")
    saveJobOutput = serializers.BooleanField(default=SAVE_OUTPUT_DEFAULT,
                                             help_text="If True, saves the output to the output dir.",
                                             source="save_job_output")

    params = serializers.DictField(help_text="Additional arguments to HuggingFace trainer.", required=False)

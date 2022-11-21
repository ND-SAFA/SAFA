from rest_enumfield import EnumField
from rest_framework import serializers

from server.serializers.job_factory.model_identifier_serializer import ModelIdentifierSerializer
from tracer.pre_processing.pre_processing_steps import PreProcessingSteps


class PreTrainingRequestSerializer(ModelIdentifierSerializer):
    trainingDataDir = serializers.CharField(max_length=200,
                                            source="training_data_dir",
                                            help_text="Path to directory containing pre-training documents.")
    preProcessingOptions = serializers.ListField(
        source='pre_processing_options',
        child=EnumField(choices=PreProcessingSteps, required=False, help_text="Custom pre-processing options."))

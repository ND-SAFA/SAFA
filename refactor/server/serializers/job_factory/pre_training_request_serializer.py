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
    blockSize = serializers.IntegerField(required=False, source="block_size",
                                         help_text="The length of a pre-training block.")
    traceArgsParams = serializers.DictField(required=False, source="trace_args_params",
                                            help_text="Custom training arguments.")
    mlmProbability = serializers.FloatField(required=False, source="mlm_probability",
                                            help_text="The probability a word in a block will be masked")

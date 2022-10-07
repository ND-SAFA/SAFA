# models.py
from rest_enumfield import EnumField
from rest_framework import serializers

from common.models.base_models.supported_base_model import SupportedBaseModel
from common.storage.safa_storage import SafaStorage
from experiment.common.run_mode import RunMode
from trace.jobs.trace_args_builder import TraceArgsBuilder


def validate_settings(value):
    """
    Check that the blog post is about Django.
    """
    for arg_name in value.keys():
        if not TraceArgsBuilder.is_a_training_arg(arg_name):
            raise serializers.ValidationError("%s is not a known Training argument" % arg_name)
    return value


class BaseTraceSerializer(serializers.Serializer):
    modelPath = serializers.CharField(max_length=255, help_text="The path to the model weights / state.")
    outputDir = serializers.CharField(max_length=255, help_text="Path to directory of output file.")
    baseModel = EnumField(choices=SupportedBaseModel, to_repr=lambda a: a, help_text="The base model class to use.",
                          default=SupportedBaseModel.BERT_FOR_MASKED_LM)

    def create(self, validated_data):
        settings = validated_data["settings"] if "settings" in validated_data else None
        return TraceArgsBuilder(base_model=validated_data["baseModel"],
                                model_path=validated_data["modelPath"],
                                output_dir=validated_data["outputDir"],
                                settings=settings)


class PredictSerializer(BaseTraceSerializer):
    sourceLayers = serializers.ListField(
        child=serializers.DictField(child=serializers.CharField()),
        help_text="List of dictionaries corresponding to the source artifacts at each layer."
    )
    targetLayers = serializers.ListField(
        child=serializers.DictField(child=serializers.CharField()),
        help_text="List of dictionaries corresponding to the target artifacts at each layer"
    )
    loadFromStorage = serializers.BooleanField(required=False,
                                               help_text="Whether model weights should reference cloud storage.",
                                               default=False)

    def create(self, validated_data):
        trace_args_builder = super().create(validated_data)
        trace_args_builder.source_layers = validated_data["sourceLayers"]
        trace_args_builder.target_layers = validated_data["targetLayers"]
        if validated_data["loadFromStorage"]:
            trace_args_builder.model_path = SafaStorage.add_mount_directory(validated_data["modelPath"])
        return trace_args_builder


class TrainSerializer(PredictSerializer):
    links = serializers.ListField(
        child=serializers.ListField(child=serializers.CharField()),
        help_text="List of true links between source and target artifacts"
    )

    def create(self, validated_data):
        trace_args_builder = super().create(validated_data)
        trace_args_builder.links = validated_data["links"]
        return trace_args_builder


class ExperimentSerializer(BaseTraceSerializer):
    run_mode = EnumField(choices=RunMode, to_repr=lambda a: a, help_text="The types of experiments to run.")

    def create(self, validated_data):
        trace_args_builder = super().create(validated_data)
        return trace_args_builder


class PreTrainSerializer(BaseTraceSerializer):
    HELP_MESSAGE = "The path to the pretraining data. Expect path to txt file or folder containing many files."
    pretrain_data_path = serializers.CharField(max_length=500,
                                               help_text=HELP_MESSAGE)

    def create(self, validated_data):
        trace_args_builder = super().create(validated_data)
        trace_args_builder.pretraining_data_path = validated_data["pretrain_data_path"]
        print("ArgBuilderDataPath:", trace_args_builder.pretraining_data_path)
        return trace_args_builder

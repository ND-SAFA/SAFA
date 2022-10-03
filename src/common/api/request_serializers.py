# models.py
from rest_enumfield import EnumField
from rest_framework import serializers

from common.models.base_models.supported_base_model import SupportedBaseModel
from trace.jobs.trace_args_builder import TraceArgsBuilder


def validate_settings(value):
    """
    Check that the blog post is about Django.
    """
    for arg_name in value.keys():
        print(arg_name, TraceArgsBuilder.is_a_training_arg(arg_name))
        if not TraceArgsBuilder.is_a_training_arg(arg_name):
            raise serializers.ValidationError("%s is not a known Training argument" % arg_name)
    return value


class BaseTraceSerializer(serializers.Serializer):
    modelPath = serializers.CharField(max_length=255)  # The path to the model weights / state.
    outputDir = serializers.CharField(max_length=255)  # Path to directory of output file.
    baseModel = EnumField(choices=SupportedBaseModel, to_repr=lambda a: a)  # The base model class to use.
    settings = serializers.DictField(required=False, validators=[validate_settings])

    def create(self, validated_data):
        return TraceArgsBuilder(base_model=validated_data["baseModel"],
                                model_path=validated_data["modelPath"],
                                output_dir=validated_data["outputDir"],
                                settings=validated_data["settings"])


class PredictSerializer(BaseTraceSerializer):
    sourceLayers = serializers.ListField(
        child=serializers.DictField(child=serializers.CharField())
    )  # List of dictionaries corresponding to the source artifacts at each layer
    targetLayers = serializers.ListField(
        child=serializers.DictField(child=serializers.CharField())
    )  # List of dictionaries corresponding to the target artifacts at each layer
    loadFromStorage = serializers.BooleanField(required=False)  # Whether model weights should reference cloud storage


class TrainSerializer(PredictSerializer):
    links = serializers.ListField(
        child=serializers.ListField(child=serializers.CharField())
    )  # List of true links between source and target artifacts

# models.py
from rest_framework import serializers

from trace.jobs.trace_args_builder import TraceArgsBuilder


class BaseTraceSerializer(serializers.Serializer):
    model_path = serializers.CharField(max_length=255)  # The path to the model weights / state.
    output_dir = serializers.CharField(max_length=255)  # Path to directory of output file.
    base_model = serializers.CharField(max_length=255)  # The base model class to use.

    def create(self, validated_data):
        return TraceArgsBuilder(**validated_data)


class PredictSerializer(BaseTraceSerializer):
    source_layers = serializers.ListField(
        child=serializers.DictField(child=serializers.CharField())
    )  # List of dictionaries corresponding to the source artifacts at each layer
    target_layers = serializers.ListField(
        child=serializers.DictField(child=serializers.CharField())
    )  # List of dictionaries corresponding to the target artifacts at each layer
    load_from_storage = serializers.BooleanField(required=False)  # Whether model weights should reference cloud storage


class TrainSerializer(PredictSerializer):
    links = serializers.ListField(
        child=serializers.ListField(child=serializers.CharField())
    )  # List of true links between source and target artifacts

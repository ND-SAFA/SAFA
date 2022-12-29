from rest_framework import serializers

from data.processing.augmentation.data_augmenter import DataAugmenter
from server.serializers.augmentation_step_serializer import AugmentationStepSerializer
from server.serializers.serializer_utility import SerializerUtility


class AugmentationSerializer(serializers.Serializer):
    """
    Responsible for creating data augmenter and its steps.
    """
    params = serializers.DictField(help_text="Construction parameters for data augmenter.")
    steps = AugmentationStepSerializer(many=True, required=True)

    def update(self, instance, validated_data):
        SerializerUtility.update_error()

    def create(self, validated_data):
        validated_data = SerializerUtility.create_children_serializers(validated_data, self.fields.fields)
        steps = validated_data["steps"]
        params = validated_data.pop("params", {})
        return DataAugmenter(steps, **params)

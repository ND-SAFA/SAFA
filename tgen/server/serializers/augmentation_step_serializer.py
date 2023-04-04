from typing import Dict, Type

from rest_enumfield import EnumField
from rest_framework import serializers

from data.processing.augmentation.abstract_data_augmentation_step import AbstractDataAugmentationStep
from data.processing.augmentation.data_augmentation_steps import AugmentationStep
from jobs.job_factory import JobFactory
from server.serializers.serializer_utility import SerializerUtility


class AugmentationStepSerializer(serializers.Serializer):
    creator = EnumField(choices=AugmentationStep, help_text="The augmentation step to perform.", required=True)
    percentToWeight = serializers.FloatField(source="percent_to_weight",
                                             help_text="The percentage of the trace links to augment.",
                                             default=1,
                                             required=False)
    params = serializers.DictField(help_text="Any construction parameters to include in construction.", default={},
                                   required=False)

    def update(self, instance: JobFactory, validated_data: Dict):
        SerializerUtility.update_error()

    def create(self, validated_data: Dict):
        creator_class: Type[AbstractDataAugmentationStep] = validated_data.pop("creator").value
        creator_params = validated_data.pop("params")
        return creator_class(**validated_data, **creator_params)

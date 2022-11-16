from typing import Dict, Type

from rest_enumfield import EnumField
from rest_framework import serializers

from server.serializers.dataset.pre_processing_step_serializer import PreProcessingStepSerializer
from tracer.datasets.creators.abstract_dataset_creator import AbstractDatasetCreator
from tracer.datasets.creators.abstract_trace_dataset_creator import AbstractTraceDatasetCreator
from tracer.datasets.creators.supported_dataset_creator import SupportedDatasetCreator
from tracer.util.reflection_util import ParamScope, ReflectionUtil


class DatasetCreatorSerializer(serializers.Serializer):
    creator = EnumField(choices=SupportedDatasetCreator,
                        help_text="The class used to create dataset.")
    params = serializers.DictField(help_text="The arguments used to construct dataset.")

    preProcessingSteps = PreProcessingStepSerializer(help_text="The steps performed on dataset before model access.",
                                                     many=True,
                                                     source="pre_processing_steps")

    def create(self, validated_data: Dict) -> AbstractTraceDatasetCreator:
        pre_processing_steps_serializer = PreProcessingStepSerializer(data=validated_data.get('pre_processing_steps'),
                                                                      many=True)
        if not pre_processing_steps_serializer.is_valid():
            raise ValueError(pre_processing_steps_serializer.errors)
        pre_processing_steps = pre_processing_steps_serializer.save()
        creator_class: Type[AbstractTraceDatasetCreator] = validated_data["creator"].value
        return creator_class(pre_processing_steps=pre_processing_steps, **validated_data["params"])

    def update(self, instance, validated_data) -> AbstractTraceDatasetCreator:
        raise NotImplementedError("Updating DatasetCreator is not valid. Please create new object")

    @staticmethod
    def get_steps(instance: AbstractDatasetCreator):
        steps = instance._pre_processor.ordered_before_steps + instance._pre_processor.ordered_regular_steps
        step_output = []
        for step in steps:
            step_output.append({
                "step": step.__class__.__name__,
                "params": ReflectionUtil.get_fields(step, ParamScope.LOCAL)
            })
        return step_output

    def to_representation(self, instance: AbstractDatasetCreator):
        steps = instance._pre_processor.steps
        s = PreProcessingStepSerializer(steps, many=True)
        s_r = s.to_representation(steps)
        return {
            "creator": ReflectionUtil.get_enum_key(SupportedDatasetCreator, instance),
            "params": ReflectionUtil.get_fields(instance, ParamScope.LOCAL),
            "preProcessingSteps": s_r
        }


class DatasetDefinitionSerializer(serializers.Serializer):
    dataset = DatasetCreatorSerializer()
    pre_processing = serializers.ListField(child=PreProcessingStepSerializer(),
                                           help_text="The list of pre-processing steps to perform on dataset.")


class DatasetMapSerializer(serializers.Serializer):
    pre_train = DatasetDefinitionSerializer(allow_null=True)
    train = DatasetDefinitionSerializer(allow_null=True)
    val = DatasetDefinitionSerializer(allow_null=True)
    eval = DatasetDefinitionSerializer(allow_null=True)

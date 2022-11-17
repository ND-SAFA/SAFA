from typing import Dict, Type

from rest_enumfield import EnumField
from rest_framework import serializers

from server.serializers.abstract_serializer import AbstractSerializer
from server.serializers.dataset.pre_processing_step_serializer import PreProcessingStepSerializer
from tracer.datasets.creators.abstract_dataset_creator import AbstractDatasetCreator
from tracer.datasets.creators.abstract_trace_dataset_creator import AbstractTraceDatasetCreator
from tracer.datasets.creators.supported_dataset_creator import SupportedDatasetCreator
from tracer.util.reflection_util import ParamScope, ReflectionUtil


class DatasetCreatorSerializer(AbstractSerializer):
    creator = EnumField(choices=SupportedDatasetCreator,
                        help_text="The class used to create dataset.")
    params = serializers.DictField(help_text="The arguments used to construct dataset.")

    preProcessingSteps = PreProcessingStepSerializer(help_text="The steps performed on dataset before model access.",
                                                     many=True,
                                                     source="pre_processing_steps")

    def create(self, validated_data: Dict) -> AbstractTraceDatasetCreator:
        kwargs = super().create(validated_data)
        pre_processing_steps = kwargs["pre_processing_steps"]
        creator_class: Type[AbstractTraceDatasetCreator] = kwargs["creator"].value
        return creator_class(pre_processing_steps=pre_processing_steps, **kwargs["params"])

    def update(self, instance, validated_data) -> AbstractTraceDatasetCreator:
        raise NotImplementedError("Updating DatasetCreator is not valid. Please create new object")

    def to_representation(self, instance: AbstractDatasetCreator):
        steps = instance._pre_processor.steps
        step_serializer = PreProcessingStepSerializer(steps, many=True)
        s_r = step_serializer.to_representation(steps)
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

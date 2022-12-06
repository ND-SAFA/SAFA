from typing import Dict

from jobs.job_factory import JobFactory
from server.serializers.augmentation_step_serializer import AugmentationStepSerializer
from server.serializers.job_factory.job_factory_converter import JobFactoryConverter
from server.serializers.job_factory.prediction_request_serializer import PredictionRequestSerializer
from server.serializers.serializer_utility import SerializerUtility


class TrainingRequestSerializer(PredictionRequestSerializer):
    """
    The serializer for training a model.
    """
    augmentationSteps = AugmentationStepSerializer(many=True, required=False, source="augmentation_steps")

    def create(self, validated_data: Dict) -> JobFactory:
        representation: Dict = SerializerUtility.create_children_serializers(validated_data, self.fields.fields)
        augmentation_steps = None
        if "augmentation_steps" in validated_data:
            augmentation_steps = representation.pop("augmentation_steps")
        SerializerUtility.serialize_trainer_dataset_container(representation, "train_dataset_creator",
                                                              augmentation_steps=augmentation_steps)
        return JobFactoryConverter.create_job_factory(representation)

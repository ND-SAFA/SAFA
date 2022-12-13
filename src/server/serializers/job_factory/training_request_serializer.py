from typing import Dict

from data.processing.augmentation.data_augmenter import DataAugmenter
from jobs.job_factory import JobFactory
from server.serializers.augmentation_serializer import AugmentationSerializer
from server.serializers.dataset.dataset_creator_serializer import DatasetCreatorSerializer
from server.serializers.job_factory.job_factory_converter import JobFactoryConverter
from server.serializers.job_factory.prediction_request_serializer import PredictionRequestSerializer
from server.serializers.serializer_utility import SerializerUtility


class TrainingRequestSerializer(PredictionRequestSerializer):
    """
    The serializer for training a model.
    """
    augmentation = AugmentationSerializer(help_text="The definition for the data augmenter.",
                                          default=None,
                                          required=False)
    val_data = DatasetCreatorSerializer(help_text="Creator for validation dataset.",
                                        required=False)

    def create(self, validated_data: Dict) -> JobFactory:
        representation: Dict = SerializerUtility.create_children_serializers(validated_data, self.fields.fields)
        data_augmenter = None
        if "augmentation" in validated_data:
            data_augmenter: DataAugmenter = representation.pop("augmentation")

        SerializerUtility.serialize_trainer_dataset_container(representation, [("data", "train_dataset_creator"),
                                                                               ("val_data", "val_dataset_creator")],
                                                              data_augmenter=data_augmenter)
        return JobFactoryConverter.create_job_factory(representation)

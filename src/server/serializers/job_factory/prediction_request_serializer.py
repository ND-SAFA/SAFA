from typing import Dict

from jobs.job_factory import JobFactory
from server.serializers.dataset.dataset_creator_serializer import DatasetCreatorSerializer
from server.serializers.job_factory.job_factory_converter import JobFactoryConverter
from server.serializers.job_factory.model_identifier_serializer import ModelIdentifierSerializer
from server.serializers.serializer_utility import SerializerUtility


class PredictionRequestSerializer(ModelIdentifierSerializer):
    """
    Serializer for a model prediction request.
    """
    data = DatasetCreatorSerializer(help_text="The instructions for creating training/prediction dataset.",
                                    required=True)

    def create(self, validated_data: Dict, dataset_param_key="eval") -> JobFactory:
        representation: Dict = SerializerUtility.create_children_serializers(validated_data, self.fields.fields)
        SerializerUtility.wrap_property_with_trainer_dataset_container(representation, dataset_param_key)
        return JobFactoryConverter.create_job_factory(representation)

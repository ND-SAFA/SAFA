from typing import Dict

from server.serializers.abstract_serializer import AbstractSerializer
from server.serializers.dataset.dataset_creator_serializer import DatasetCreatorSerializer
from tracer.datasets.trainer_datasets_container import TrainerDatasetsContainer


class TrainerDatasetsContainerSerializer(AbstractSerializer):
    preTrain = DatasetCreatorSerializer(help_text="The instructions for creating pre-training dataset.",
                                        required=False,
                                        source="pre_train")
    train = DatasetCreatorSerializer(help_text="The instructions for creating training dataset.",
                                     required=False)
    val = DatasetCreatorSerializer(help_text="The instructions for creating validation dataset.",
                                   required=False)
    eval = DatasetCreatorSerializer(help_text="The instructions for creating testing dataset.",
                                    required=False)

    def update(self, instance, validated_data):
        raise NotImplementedError("Updating is not supported. Please create new object.")

    def create(self, validated_data: Dict):
        kwargs = super().create(validated_data)
        return TrainerDatasetsContainer(**kwargs)

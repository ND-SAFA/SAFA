from django.test import TestCase

from server.serializers.dataset.trainer_dataset_container_serializer import TrainerDatasetsContainerSerializer
from server.serializers.tests.base_serializer_test import BaseSerializerTest
from tracer.datasets.trainer_datasets_container import TrainerDatasetsContainer


class TestPreProcessingStepSerializer(TestCase):
    test_data = {
        "preTrain": {
            "creator": "MLM_PRETRAIN",
            "params": {
                "orig_data_path": "/mnt/datasets/automotive"
            },
            "preProcessingSteps": [
                {
                    "step": "FILTER_MIN_LENGTH",
                    "params": {
                        "min_length": 10
                    }
                }
            ]
        },
        "train": {
            "creator": "SAFA",
            "params": {
                "project_path": "/mnt/datasets/LHP"
            },
            "preProcessingSteps": [
                {
                    "step": "REMOVE_WHITE_SPACE",
                }
            ]
        }
    }

    serializer_test = BaseSerializerTest(TrainerDatasetsContainerSerializer)

    def test_serialization(self):
        entity: TrainerDatasetsContainer = self.serializer_test.serialize_data(self, self.test_data)
        self.assertIsNotNone(entity.pre_train_dataset)
        self.assertIsNotNone(entity.train_dataset)
        self.assertIsNone(entity.eval_dataset)
        self.assertIsNone(entity.val_dataset)

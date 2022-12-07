from server.serializers.dataset.trainer_dataset_container_serializer import TrainerDatasetsContainerSerializer
from server.serializers.tests.base_serializer_test import BaseSerializerTest
from test.base_test import BaseTest
from data.datasets.dataset_role import DatasetRole
from data.datasets.trainer_dataset_manager import TrainerDatasetManager
import unittest


@unittest.skip("Needs Fixed")
class TestPreProcessingStepSerializer(BaseTest):
    test_data = {
        "preTrain": {
            "creator": "MLM_PRETRAIN",
            "params": {
                "orig_data_path": "/mnt/data/automotive"
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
                "project_path": "/mnt/data/LHP"
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
        entity: TrainerDatasetManager = self.serializer_test.serialize_data(self, self.test_data)
        self.assertIsNotNone(entity[DatasetRole.PRE_TRAIN])
        self.assertIsNotNone(entity[DatasetRole.TRAIN])
        self.assertIsNone(entity[DatasetRole.EVAL])
        self.assertIsNone(entity[DatasetRole.VAL])

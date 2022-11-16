from django.test import TestCase

from server.serializers.dataset.dataset_container_serializer import TrainerDatasetsContainerSerializer
from server.serializers.tests.base_serializer_test import BaseSerializerTest


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
        entity = self.serializer_test.serialize_data(self, self.test_data)
        BaseSerializerTest.assert_contains_camel_case_properties(self, entity, self.test_data["params"])

    # def test_deserialization(self):
    #     self.serializer_test.serialize_deserialize_data(self, self.test_data)
    #
    # def test_update(self):
    #     new_properties = {"params": {"min_length": 20}}
    #     expected_properties = new_properties["params"]
    #     self.serializer_test.serialize_update_data(self, self.test_data, new_properties, expected_properties)
    #
    # def test_invalid_update(self):
    #     invalid_properties = {"step": "test"}
    #     self.serializer_test.test_invalid_update(self, self.test_data, invalid_properties)
    #
    # def test_serialization_with_no_params(self):
    #     test_data = {"step": "REMOVE_WHITE_SPACE"}
    #     entity = self.serializer_test.serialize_data(self, test_data)
    #     BaseSerializerTest.assert_contains_camel_case_properties(self, entity, self.test_data["params"])

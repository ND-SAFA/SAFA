from server.serializers.dataset.dataset_creator_serializer import DatasetCreatorSerializer
from server.serializers.tests.base_serializer_test import BaseSerializerTest
from test.base_test import BaseTest
import unittest


@unittest.skip("Needs Fixed")
class TestDatasetCreatorSerializer(BaseTest):
    test_data = {
        "creator": "CSV",
        "params": {
            "data_file_path": "hello"
        },
        "preProcessingSteps": [
            {
                "step": "FILTER_MIN_LENGTH",
                "params": {
                    "min_length": 10
                }
            }
        ]
    }

    serializer_test = BaseSerializerTest(DatasetCreatorSerializer)

    def test_serialization(self):
        training_request = self.serializer_test.serialize_data(self, self.test_data)
        BaseSerializerTest.assert_contains_camel_case_properties(self, training_request, self.test_data["params"])

    def test_deserialization(self):
        self.serializer_test.serialize_deserialize_data(self, self.test_data)

    def test_update_throws_error(self):
        new_properties = {"creator": "SAFA"}
        try:
            self.serializer_test.test_no_update(self, self.test_data, new_properties)
            self.fail("Update should not be possible")
        except NotImplementedError as e:
            pass

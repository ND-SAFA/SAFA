from jobs.job_factory import JobFactory
from server.serializers.job_factory.prediction_request_serializer import PredictionRequestSerializer
from server.serializers.tests.base_serializer_test import BaseSerializerTest
from test.base_test import BaseTest
from data.datasets.dataset_role import DatasetRole
import unittest


@unittest.skip("Needs Fixed")
class TestPredictionRequestSerializer(BaseTest):
    """
    Test that the PredictionRequestSerializer is able to create PredictionRequest from JSON and export PredictionRequest
    as JSON
    """
    serializer_test_data = {
        "baseModel": "NL_BERT",
        "modelPath": "~/desktop/safa/data",
        "outputDir": "hello",
        "data": {
            "creator": "CLASSIC_TRACE",
            "params": {
                "source_layers": [{"S1": "hello"}],
                "target_layers": [{"T1": "world"}]
            }
        },
        "params": {
            "num_train_epochs": 1
        }
    }
    serializer_test = BaseSerializerTest(PredictionRequestSerializer)

    def test_serialization(self):
        prediction_request: JobFactory = self.serializer_test.serialize_data(self, self.serializer_test_data)
        self.assertIsNotNone(prediction_request.trainer_dataset_container)
        self.assertIsNotNone(prediction_request.trainer_dataset_container[DatasetRole.EVAL])
        BaseSerializerTest.assert_contains_camel_case_properties(self, prediction_request, self.serializer_test_data)

    def test_deserialization(self):
        self.serializer_test.serialize_deserialize_data(self, self.serializer_test_data)

    def test_no_update(self):
        new_properties = {"outputDir": "hello world"}

        def run_update():
            self.serializer_test.test_no_update(self, self.serializer_test_data, new_properties)

        self.assertRaises(NotImplementedError, run_update)

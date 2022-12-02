from jobs.job_factory import JobFactory
from server.serializers.job_factory.training_request_serializer import TrainingRequestSerializer
from server.serializers.tests.base_serializer_test import BaseSerializerTest
from test.base_test import BaseTest
from data.datasets.dataset_role import DatasetRole
from util.reflection_util import ReflectionUtil
import unittest


@unittest.skip("Needs Fixed")
class TestTrainingRequestSerializer(BaseTest):
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
                "target_layers": [{"T1": "world"}],
                "true_links": [["S1", "T1"]]
            }
        },
        "params": {
            "num_train_epochs": 1
        }
    }

    serializer_test = BaseSerializerTest(TrainingRequestSerializer)

    def test_serialization(self):
        job_factory: JobFactory = self.serializer_test.serialize_data(self, self.serializer_test_data)
        dataset_container = job_factory.trainer_dataset_container
        self.assertIsNotNone(dataset_container)
        self.assertIsNotNone(dataset_container[DatasetRole.TRAIN])
        # Verify that general properties have been set
        expected_properties = ReflectionUtil.copy_fields(self.serializer_test_data,
                                                         exclude=["data", "settings", "params"])
        BaseSerializerTest.assert_contains_camel_case_properties(self, job_factory, expected_properties)

        # Verify that settings have been set
        expected_settings_properties = self.serializer_test_data["params"]
        BaseSerializerTest.assert_contains_camel_case_properties(self, job_factory.additional_job_params,
                                                                 expected_settings_properties)

    def test_deserialization(self):
        expected_properties = ReflectionUtil.copy_fields(self.serializer_test_data, exclude=["data", "settings"])
        self.serializer_test.serialize_deserialize_data(self, self.serializer_test_data)

    def test_update(self):
        new_properties = {"outputDir": "hello"}

        def update_runner():
            self.serializer_test.test_no_update(self,
                                                self.serializer_test_data,
                                                new_properties)

        self.assertRaises(NotImplementedError, update_runner)

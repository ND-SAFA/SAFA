from django.test import TestCase

from jobs.job_factory import JobFactory
from server.serializers.job_factory.training_request_serializer import TrainingRequestSerializer
from server.serializers.tests.base_serializer_test import BaseSerializerTest
from tracer.util.reflection_util import ReflectionUtil


class TestTrainingRequestSerializer(TestCase):
    """
    Test that the PredictionRequestSerializer is able to create PredictionRequest from JSON and export PredictionRequest
    as JSON
    """
    serializer_test_data = {
        "baseModel": "NL_BERT",
        "modelPath": "~/desktop/safa/datasets",
        "outputDir": "hello",
        "data": {
            "creator": "CLASSIC_TRACE",
            "params": {
                "source_layers": [{"S1": "hello"}],
                "target_layers": [{"T1": "world"}],
                "true_links": [["S1", "T1"]]
            }
        },
        "settings": {
            "num_train_epochs": 1
        }
    }

    serializer_test = BaseSerializerTest(TrainingRequestSerializer)

    def test_serialization(self):
        job_factory: JobFactory = self.serializer_test.serialize_data(self, self.serializer_test_data)
        dataset_container = job_factory.trainer_dataset_container
        self.assertIsNotNone(dataset_container)
        self.assertIsNotNone(dataset_container.train_dataset)
        # Verify that general properties have been set
        expected_properties = ReflectionUtil.copy_fields(self.serializer_test_data, exclude=["data", "settings"])
        BaseSerializerTest.assert_contains_camel_case_properties(self, job_factory, expected_properties)

        # Verify that settings have been set
        expected_settings_properties = self.serializer_test_data["settings"]
        BaseSerializerTest.assert_contains_camel_case_properties(self, job_factory.additional_job_params,
                                                                 expected_settings_properties)

    def test_deserialization(self):
        expected_properties = ReflectionUtil.copy_fields(self.serializer_test_data, exclude=["data", "settings"])
        self.serializer_test.serialize_deserialize_data(self, self.serializer_test_data)

    def test_update(self):
        new_properties = {"true_": [["T1", "S1"]]}
        self.serializer_test.serialize_update_data(self, self.serializer_test_data, new_properties)

    def test_invalid_update(self):
        invalid_properties = {"links": "test"}
        self.serializer_test.test_invalid_update(self, self.serializer_test_data, invalid_properties,
                                                 expected_phrase="list")

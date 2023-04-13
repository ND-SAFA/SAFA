from api.serializers.prediction_serializer import PredictionSerializer
from api.serializers.tests.test_dataset_serializer import TestDatasetSerializer
from api.tests.api_base_test import ApiBaseTest


class TestPredictionSerializer(ApiBaseTest):
    """
    Tests that prediction payload can be serialized.
    """

    def test_pos_serialization(self):
        """
        Tests that valid payload is able to be serialized.
        """
        model_name = "thearod5/pl-bert"
        payload = {
            "model": model_name,
            "dataset": TestDatasetSerializer.dataset_payload
        }
        serializer = PredictionSerializer(data=payload)
        self.assertTrue(serializer.is_valid())
        data = serializer.save()
        self.assertEqual(model_name, data["model"])
        TestDatasetSerializer.assert_valid_dataset(self, data["dataset"])

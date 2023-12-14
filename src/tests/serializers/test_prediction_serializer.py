from api.endpoints.views.predict_serializer import PredictionSerializer
from tests.base_test import BaseTest
from tests.common.test_data import TestData, TestSubset


class TestPredictionSerializer(BaseTest):
    """
    Tests that prediction payload can be serialized.
    """

    def test_pos_serialization(self):
        """
        Serializes dataset and verifies that serializes correctly constructs dataset entities.
        """
        for data_subset in TestSubset:
            data = {"dataset": TestData.get_dataset(data_subset, encode=True)}
            serializer = PredictionSerializer(data=data)
            self.assertTrue(serializer.is_valid(raise_exception=True))
            data = serializer.save()
            dataset_data = data["dataset"]
            TestData.verify_dataset(self, dataset_data, data_subset)

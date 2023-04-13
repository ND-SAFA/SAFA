from dotenv import load_dotenv
from tgen.src.server.api.api_definition import ApiDefinition

from api.serializers.dataset_serializer import DatasetSerializer
from api.tests.api_base_test import ApiBaseTest
from api.tests.test_data import TestData

load_dotenv()


class TestDatasetSerializer(ApiBaseTest):
    """
    Tests that datasets are able to be serialized.
    """

    def test_pos_serialization(self):
        """
        Tests that a valid example is serialized correctly.
        """
        serializer = DatasetSerializer(data=TestData.dataset)
        self.assertTrue(serializer.is_valid())

        dataset: ApiDefinition = serializer.save()
        TestData.assert_valid_dataset(self, dataset)

    def test_neg_serialization(self):
        """
        Tests that invalid payload results in invalid serializer state.
        """
        payload = {}
        serializer = DatasetSerializer(data=payload)
        self.assertFalse(serializer.is_valid())

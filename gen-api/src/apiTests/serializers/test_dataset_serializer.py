from dotenv import load_dotenv

from api.endpoints.gen.serializers.dataset_serializer import DatasetSerializer
from apiTests.base_test import BaseTest
from apiTests.common.test_data import TestData, TestSubset
from gen_common.data.readers.definitions.api_definition import ApiDefinition

load_dotenv()


class TestDatasetSerializer(BaseTest):
    """
    Tests that datasets are able to be serialized.
    """

    def test_pos_serialization(self):
        """
        Tests that a valid example is serialized correctly.
        """
        for subset in TestSubset:
            dataset = TestData.get_dataset(subset, encode=True)
            serializer = DatasetSerializer(data=dataset)
            self.assertTrue(serializer.is_valid())

            dataset: ApiDefinition = serializer.save()
            TestData.verify_dataset(self, dataset, subset)

    def test_neg_serialization(self):
        """
        Tests that invalid payload results in invalid serializer state.
        """
        payload = {}
        serializer = DatasetSerializer(data=payload)
        self.assertFalse(serializer.is_valid())

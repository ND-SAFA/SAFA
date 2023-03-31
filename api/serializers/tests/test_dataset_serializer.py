from typing import TypedDict
from unittest import TestCase

from dotenv import load_dotenv

from serializers.dataset_serializer import DatasetSerializer
from tests.api_base_test import ApiBaseTest
from tgen.src.server.api.api_definition import ApiDefinition

load_dotenv()


class TestDatasetSerializer(ApiBaseTest):
    """
    Tests that datasets are able to be serialized.
    """
    dataset_payload = {
        "source_layers": [
            {"A": "I am the first letter of the alphabet."}
        ],
        "target_layers": [
            {"B": "I am the second letter of the alphabet."}
        ]
    }

    def test_pos_serialization(self):
        """
        Tests that a valid example is serialized correctly.
        """
        serializer = DatasetSerializer(data=self.dataset_payload)
        self.assertTrue(serializer.is_valid())

        dataset: ApiDefinition = serializer.save()
        self.assert_valid_dataset(dataset)

    def test_neg_serialization(self):
        """
        Tests that invalid payload results in invalid serializer state.
        """
        payload = {}
        serializer = DatasetSerializer(data=payload)
        self.assertFalse(serializer.is_valid())

    @staticmethod
    def assert_valid_dataset(test_case: TestCase, dataset: TypedDict) -> None:
        """
        Verifies that dataset contains equal amount of source/target layers and artifacts are defined.
        :param test_case: The test case to make assertions with.
        :param dataset: The dataset to verify.
        :return:None
        """
        test_case.assertEqual(1, len(dataset["source_layers"]))
        test_case.assertIn("A", dataset["source_layers"][0])
        test_case.assertEqual(1, len(dataset["target_layers"]))
        test_case.assertIn("B", dataset["target_layers"][0])

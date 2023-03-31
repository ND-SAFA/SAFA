from typing import Dict
from unittest import TestCase


class TestData:
    """
    Holds data used for creating single integrated test.
    """
    dataset = {
        "source_layers": [
            {"A": "I am the first letter of the alphabet."}
        ],
        "target_layers": [
            {"B": "I am the second letter of the alphabet."}
        ]
    }

    @staticmethod
    def assert_valid_dataset(test_case: TestCase, dataset: Dict) -> None:
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

from typing import Dict, Union
from unittest import TestCase

from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame
from tgen.data.readers.definitions.api_definition import ApiDefinition
from tgen.testres.test_assertions import TestAssertions


class TestData:
    """
    Holds data used for creating single integrated test.
    """
    dataset = {
        "artifacts": [
            {
                "id": "A1",
                "content": "I am the first letter of the alphabet.",
                "summary": "This is a summary of the artifact",
                "layer_id": "A"
            },
            {
                "id": "B1",
                "content": "I am the second letter of the alphabet.",
                "layer_id": "B",
                "summary": ""
            }
        ],
        "layers": [{"parent": "A", "child": "B"}]
    }

    @staticmethod
    def assert_valid_dataset(tc: TestCase, dataset: Union[ApiDefinition, Dict]) -> None:
        """
        Verifies that dataset contains equal amount of source/target layers and artifacts are defined.
        :param tc: The test case to make assertions with.
        :param dataset: The dataset to verify.
        :return:None
        """
        if isinstance(dataset, Dict):
            dataset = ApiDefinition(**dataset)

        tc.assertEqual(2, len(dataset.artifacts))
        artifact_df = ArtifactDataFrame(dataset.artifacts)
        TestAssertions.verify_entities_in_df(tc, dataset.artifacts, artifact_df)

        trace_layer = dataset.layers[0]
        tc.assertEqual("A", trace_layer.parent)
        tc.assertEqual("B", trace_layer.child)

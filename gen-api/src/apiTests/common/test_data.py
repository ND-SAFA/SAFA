from enum import Enum
from typing import Any, Dict, List, Union
from unittest import TestCase

import pandas as pd

from apiTests.common.data_encoder import DataEncoder
from apiTests.common.test_constants import CHILD_TYPE, FR_ARTIFACT_PATH, PARENT_TYPE, SOURCE_CODE_PATH, SUMMARY_JSON_PATH, SUMMARY_PATH
from tgen.common.objects.artifact import Artifact
from tgen.common.objects.trace_layer import TraceLayer
from tgen.common.util.enum_util import EnumDict
from tgen.common.util.file_util import FileUtil
from tgen.common.util.json_util import JsonUtil
from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame
from tgen.data.keys.structure_keys import ArtifactKeys
from tgen.data.readers.definitions.api_definition import ApiDefinition


class TestSubset(Enum):
    """
    Defines the acceptable subsets of the test data.
    """
    SOURCE = "source"
    FULL = "full"


class TestArtifacts(Enum):
    """
    Defines the artifacts available in the test dataset.
    """
    CHILD = SOURCE_CODE_PATH
    PARENT = FR_ARTIFACT_PATH


subset2artifacts = {TestSubset.SOURCE: 4, TestSubset.FULL: 6}

IGNORED_ARTIFACT_COLS = {"chunks"}


class TestData:
    """
    Holds data used for creating single integrated test.
    """

    @staticmethod
    def get_dataset(subset: TestSubset, encode: bool = False) -> ApiDefinition:
        """
        Constructs dataset containing only source code.
        :return:
        """
        artifacts = TestData.get_artifacts_for_subset(subset)
        summary = TestData.read_summary()
        layers = [TraceLayer(parent=PARENT_TYPE, child=CHILD_TYPE)] if subset == TestSubset.FULL else []
        data = ApiDefinition(artifacts=artifacts, layers=layers, summary=summary)
        if encode:
            data = DataEncoder.encode(data)
        return data

    @staticmethod
    def read_artifacts(artifact_type: TestArtifacts) -> List[Artifact]:
        """
        Constructs list of artifacts from artifact file.
        :param artifact_type: The type of artifact to read.
        :return: The list of artifacts defined in file.
        """
        artifact_path = artifact_type.value
        code_df = pd.read_csv(artifact_path)
        artifact_df = ArtifactDataFrame(code_df)
        return artifact_df.to_artifacts()

    @staticmethod
    def read_summary(as_json: bool = False) -> Union[str, Dict]:
        """
        :param as_json: Return JSON project summary. Txt is default.
        :return: The project summary of the test dataset.
        """
        return JsonUtil.read_json_file(SUMMARY_JSON_PATH) if as_json else FileUtil.read_file(SUMMARY_PATH)

    @staticmethod
    def get_artifacts_for_subset(subset: TestSubset) -> List[Artifact]:
        """
        Reads the artifacts associated with subset.
        :param subset: The subset of the data to retrieve artifacts for.
        :return: The list of artifacts.
        """
        artifacts = TestData.read_artifacts(TestArtifacts.CHILD)
        if subset == TestSubset.FULL:
            parent_artifacts = TestData.read_artifacts(TestArtifacts.PARENT)
            artifacts.extend(parent_artifacts)
        return artifacts

    @staticmethod
    def verify_dataset(tc: TestCase, dataset: Any, subset: TestSubset) -> None:
        """
        Verifies that data contains the dataset information.
        :param tc: The test case used to make assertions.
        :param dataset: The data to verify.
        :param subset: The expected subset of the data.
        :return: None
        """
        tc.assertTrue(isinstance(dataset, ApiDefinition))

        TestData.verify_artifacts(tc, dataset.artifacts, subset)

        if subset == TestSubset.FULL:
            TestData.verify_layers(tc, dataset.layers)

    @staticmethod
    def verify_artifacts(tc: TestCase, artifacts: List[Dict], subset: TestSubset) -> None:
        """
        Verifies that artifacts match those of subset.
        :param tc: The test case used to make assertions.
        :param artifacts: The artifacts being verified.
        :param subset: The expected subset of the artifacts.
        :return: None
        """
        expected_artifacts = TestData.get_artifacts_for_subset(subset)
        tc.assertEqual(len(expected_artifacts), len(artifacts))
        for a in artifacts:
            tc.assertTrue(isinstance(a, EnumDict))
            artifact_query = [expected_artifact for expected_artifact in expected_artifacts
                              if expected_artifact[ArtifactKeys.ID] == a[ArtifactKeys.ID]]
            tc.assertEqual(len(artifact_query), 1)
            expected_artifact = artifact_query[0]
            for k, v in expected_artifact.items():
                if v is None:
                    if k not in a:
                        tc.assertIn(k, IGNORED_ARTIFACT_COLS)
                        continue
                    tc.assertIsNone(a.get(k))
                if isinstance(v, str):
                    tc.assertEqual(v.strip(), a[k].strip())
                else:
                    tc.assertEqual(v, a[k])

    @staticmethod
    def verify_layers(tc: TestCase, layers: List[Dict]) -> None:
        """
        Verifies that layers match that of test dataset.
        :param tc: The test case used to make assertions.
        :param layers: The layers to verify.
        :return: None
        """
        tc.assertEqual(len(layers), 1)
        layer = layers[0]
        assert isinstance(layer, TraceLayer)
        tc.assertTrue(isinstance(layer, TraceLayer))
        tc.assertEqual(layer.parent, PARENT_TYPE)
        tc.assertEqual(layer.child, CHILD_TYPE)

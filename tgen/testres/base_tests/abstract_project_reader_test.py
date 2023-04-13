from collections import namedtuple
from typing import Dict, List
from unittest import mock

from tgen.data.dataframes.artifact_dataframe import ArtifactKeys
from tgen.data.readers.abstract_project_reader import AbstractProjectReader
from tgen.data.summarizer.summarizer import Summarizer
from tgen.testres.base_tests.base_test import BaseTest
from tgen.testres.test_assertions import TestAssertions
from tgen.testres.testprojects.abstract_test_project import AbstractTestProject

Choice = namedtuple("Choice", ["text"])

SUMMARY_FORMAT = "Summary of {}"


def fake_open_ai_completion(model, prompt, **args):
    tokens = ["\'".join(p['prompt'].split('\'')[1:-1]) for p in prompt]
    return {"choices": [Choice(SUMMARY_FORMAT.format(token)) for token in tokens]}


class AbstractProjectReaderTest(BaseTest):
    """
    Tests that project reader is able to construct dataset frames from project data.
    """

    def verify_project_data_frames(self, test_project: AbstractTestProject) -> None:
        """
        Verifies that entries are found in data frames created by project reader.
        :param test_project: Project containing entities to compare data frames to.
        :return: None
        """
        project_reader = test_project.get_project_reader()
        artifact_df, trace_df, layer_mapping_df = project_reader.read_project()
        TestAssertions.verify_entities_in_df(self, test_project.get_artifact_entries(), artifact_df)
        TestAssertions.verify_entities_in_df(self, test_project.get_trace_entries(), trace_df)
        TestAssertions.verify_entities_in_df(self, test_project.get_layer_mapping_entries(), layer_mapping_df)

    @mock.patch("openai.Completion.create", )
    def verify_summarization(self, mock_completion: mock.MagicMock, test_project):
        """
        Verifies that entries are properly summarized by reader
        :param test_project: Project containing entities to compare data frames to.
        :return: None
        """
        mock_completion.side_effect = fake_open_ai_completion
        project_reader: AbstractProjectReader = test_project.get_project_reader()
        project_reader.set_summarizer(Summarizer())
        artifact_df, trace_df, layer_mapping_df = project_reader.read_project()
        summary_artifacts = test_project.get_artifact_entries()
        for row in summary_artifacts:
            row[ArtifactKeys.CONTENT.value] = SUMMARY_FORMAT.format(row[ArtifactKeys.CONTENT.value])
        TestAssertions.verify_entities_in_df(self, summary_artifacts, artifact_df)
        TestAssertions.verify_entities_in_df(self, test_project.get_trace_entries(), trace_df)
        TestAssertions.verify_entities_in_df(self, test_project.get_layer_mapping_entries(), layer_mapping_df)

    @staticmethod
    def generate_artifact_entries(artifact_ids: List[int], prefix: str = "None") -> List[Dict]:
        """
        Generates artifact for each index with given prefix.
        :param artifact_ids: The artifact ids to create artifacts for.
        :param prefix: The prefix to use before the artifact index in the artifact id.
        :return: List of artifact entries.
        """
        return [{
            "id": f"{prefix}{i}",
            "content": f"{prefix}_token{i}"
        } for i in artifact_ids]

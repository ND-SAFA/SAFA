from typing import Dict, List

from gen_common.data.keys.structure_keys import ArtifactKeys
from gen_common.data.readers.abstract_project_reader import AbstractProjectReader
from gen_common.summarize.artifact.artifacts_summarizer import ArtifactsSummarizer
from gen_common_test.base.constants import SUMMARY_FORMAT
from gen_common_test.base.tests.base_test import BaseTest
from gen_common_test.testprojects.abstract_test_project import AbstractTestProject


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
        layer_entries = test_project.get_layer_entries()
        self.verify_entities_in_df(test_project.get_artifact_entries(), artifact_df)
        self.verify_entities_in_df(test_project.get_trace_entries(), trace_df)
        self.verify_entities_in_df(layer_entries, layer_mapping_df)

    def verify_summarization(self, test_project: AbstractTestProject):
        """
        Verifies that entries are properly summarized by reader
        :param ai_manager: The manager responsible for specifying LLM responses. Uses dependency injection.
        :param test_project: Project containing entities to compare data frames to.
        :return: None
        """
        project_reader: AbstractProjectReader = test_project.get_project_reader()
        project_reader.set_summarizer(ArtifactsSummarizer(summarize_code_only=False))
        artifact_df, trace_df, layer_mapping_df = project_reader.read_project()
        summary_artifacts = test_project.get_artifact_entries()
        for row in summary_artifacts:
            row[ArtifactKeys.SUMMARY.value] = SUMMARY_FORMAT.format(row[ArtifactKeys.CONTENT.value])
        self.verify_entities_in_df(summary_artifacts, artifact_df)
        self.verify_entities_in_df(test_project.get_trace_entries(), trace_df)
        layer_dicts = [{"source_type": l.child, "target_type": l.parent} for l in test_project.get_trace_layers()]
        self.verify_entities_in_df(layer_dicts, layer_mapping_df)

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

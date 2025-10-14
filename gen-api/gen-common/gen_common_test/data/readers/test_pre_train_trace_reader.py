import os
from typing import List

from gen_common.data.keys.structure_keys import ArtifactKeys, TraceKeys
from gen_common.data.readers.pre_train_trace_reader import PreTrainTraceReader
from gen_common.summarize.artifact.artifacts_summarizer import ArtifactsSummarizer
from gen_common.util.file_util import FileUtil
from gen_common_test.base.constants import SUMMARY_FORMAT
from gen_common_test.base.mock.decorators.anthropic import mock_anthropic
from gen_common_test.base.mock.test_ai_manager import TestAIManager
from gen_common_test.base.paths.project_paths import GEN_COMMON_TEST_PROJECT_PRETRAIN_PATH
from gen_common_test.base.tests.base_test import BaseTest


class TestPreTrainingTraceReader(BaseTest):
    """
    Tests that csv project is correctly parsed.
    """

    @mock_anthropic
    def test_summarization(self, ai_manager: TestAIManager):
        """
        Tests that pre-train data can be summarized
        """
        ai_manager.mock_summarization()
        reader: PreTrainTraceReader = self.get_project_reader()
        reader.set_summarizer(
            ArtifactsSummarizer(summarize_code_only=False))
        artifact_df, trace_df, layer_mapping_df = reader.read_project()
        orig_lines = list(FileUtil.read_file(reader.data_file).split(os.linesep))
        summarized = [SUMMARY_FORMAT.format(line) for line in orig_lines]
        self.verify_project_data_frames(artifact_df, trace_df, layer_mapping_df, orig_lines, summarized)

    def test_read_project(self):
        """
        Tests that the csv project can be read and translated to data frames.
        """
        reader: PreTrainTraceReader = self.get_project_reader()
        artifact_df, trace_df, layer_mapping_df = reader.read_project()
        lines = FileUtil.read_file(reader.data_file).split(os.linesep)
        self.verify_project_data_frames(artifact_df, trace_df, layer_mapping_df, lines)

    @staticmethod
    def get_project_path() -> str:
        """
        :return: Returns path to CSV test project.
        """
        return GEN_COMMON_TEST_PROJECT_PRETRAIN_PATH

    @classmethod
    def get_project_reader(cls) -> PreTrainTraceReader:
        """
        :return: Returns csv reader for project.
        """
        return PreTrainTraceReader(cls.get_project_path())

    def verify_project_data_frames(self, artifact_df, traces_df, layer_df, lines, summarized_lines: List = None) -> None:
        """
        Verifies dataframes are as expected
        :return: None
        """

        def compare_lines(expected_lines, column):
            expected = expected_lines[i].strip()
            result = row[column].strip()
            self.assertEqual(expected, result)

        with open(self.get_project_path()) as file:
            expected_artifacts = file.readlines()
        self.assertEqual(len(expected_artifacts), len(artifact_df.index))
        self.assertEqual(len(traces_df[traces_df[TraceKeys.LABEL] == 1]), len(traces_df[traces_df[TraceKeys.LABEL] == 0]))
        for i, row in artifact_df.itertuples():
            compare_lines(lines, ArtifactKeys.CONTENT)
            if summarized_lines:
                compare_lines(summarized_lines, ArtifactKeys.SUMMARY)

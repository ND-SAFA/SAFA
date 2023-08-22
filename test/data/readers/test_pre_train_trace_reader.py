import os

from typing import List

from tgen.common.util.file_util import FileUtil
from tgen.core.args.open_ai_args import OpenAIArgs
from tgen.data.dataframes.artifact_dataframe import ArtifactKeys
from tgen.data.dataframes.trace_dataframe import TraceKeys
from tgen.data.readers.pre_train_trace_reader import PreTrainTraceReader
from tgen.summarizer.artifacts_summarizer import ArtifactsSummarizer
from tgen.models.llm.open_ai_manager import OpenAIManager
from tgen.testres.base_tests.base_test import BaseTest
from tgen.testres.paths.project_paths import PRE_TRAIN_TRACE_PATH
from tgen.testres.mocking.mock_openai import mock_openai
from tgen.testres.mocking.test_open_ai_responses import SUMMARY_FORMAT
from tgen.testres.mocking.test_response_manager import TestAIManager


class TestPreTrainingTraceReader(BaseTest):
    """
    Tests that csv project is correctly parsed.
    """

    def test_read_project(self):
        """
        Tests that the csv project can be read and translated to data frames.
        """
        reader: PreTrainTraceReader = self.get_project_reader()
        artifact_df, trace_df, layer_mapping_df = reader.read_project()
        lines = FileUtil.read_file(reader.data_file).split(os.linesep)
        self.verify_project_data_frames(artifact_df, trace_df, layer_mapping_df, lines)

    @mock_openai
    def test_summarization(self, ai_manager: TestAIManager):
        """
        Tests that pre-train data can be summarized
        """
        ai_manager.mock_summarization()
        reader: PreTrainTraceReader = self.get_project_reader()
        llm_manager = OpenAIManager(OpenAIArgs())
        reader.set_summarizer(ArtifactsSummarizer(llm_manager, code_or_exceeds_limit_only=False))
        artifact_df, trace_df, layer_mapping_df = reader.read_project()
        orig_lines = list(FileUtil.read_file(reader.data_file).split(os.linesep))
        summarized = [SUMMARY_FORMAT.format(line) for line in orig_lines]
        self.verify_project_data_frames(artifact_df, trace_df, layer_mapping_df, orig_lines, summarized)

    @staticmethod
    def get_project_path() -> str:
        """
        :return: Returns path to CSV test project.
        """
        return PRE_TRAIN_TRACE_PATH

    @classmethod
    def get_project_reader(cls) -> PreTrainTraceReader:
        """
        :return: Returns csv reader for project.
        """
        return PreTrainTraceReader(cls.get_project_path())

    def verify_project_data_frames(self, artifacts_df, traces_df, layer_df, lines, summarized_lines: List = None) -> None:
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
        self.assertEqual(len(expected_artifacts), len(artifacts_df.index))
        self.assertEqual(len(traces_df[traces_df[TraceKeys.LABEL] == 1]), len(traces_df[traces_df[TraceKeys.LABEL] == 0]))
        for i, row in artifacts_df.itertuples():
            compare_lines(lines, ArtifactKeys.CONTENT)
            if summarized_lines:
                compare_lines(summarized_lines, ArtifactKeys.SUMMARY)

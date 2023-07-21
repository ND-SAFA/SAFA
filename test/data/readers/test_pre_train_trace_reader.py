import os

from tgen.data.dataframes.artifact_dataframe import ArtifactKeys
from tgen.data.dataframes.trace_dataframe import TraceKeys
from tgen.data.readers.pre_train_trace_reader import PreTrainTraceReader
from tgen.data.summarizer.summarizer import Summarizer
from tgen.models.llm.open_ai_manager import OpenAIManager
from tgen.testres.base_tests.base_test import BaseTest
from tgen.testres.paths.project_paths import PRE_TRAIN_TRACE_PATH
from tgen.testres.test_anthropic_responses import mock_openai
from tgen.testres.test_open_ai_responses import SUMMARY_FORMAT
from tgen.train.args.open_ai_args import OpenAIArgs
from tgen.util.file_util import FileUtil


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
    def test_summarization(self):
        """
        Tests that pre-train data can be summarized
        """
        reader: PreTrainTraceReader = self.get_project_reader()
        llm_manager = OpenAIManager(OpenAIArgs())
        reader.set_summarizer(Summarizer(llm_manager, code_or_exceeds_limit_only=False))
        artifact_df, trace_df, layer_mapping_df = reader.read_project()
        lines = [SUMMARY_FORMAT.format(line) for line in FileUtil.read_file(reader.data_file).split(os.linesep)]
        self.verify_project_data_frames(artifact_df, trace_df, layer_mapping_df, lines)

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

    def verify_project_data_frames(self, artifacts_df, traces_df, layer_df, lines) -> None:
        """
        Verifies dataframes are as expected
        :return: None
        """
        with open(self.get_project_path()) as file:
            expected_artifacts = file.readlines()
        self.assertEqual(len(expected_artifacts), len(artifacts_df.index))
        self.assertEqual(len(traces_df[traces_df[TraceKeys.LABEL] == 1]), len(traces_df[traces_df[TraceKeys.LABEL] == 0]))
        for i, row in artifacts_df.itertuples():
            self.assertEqual(lines[i].strip(), row[ArtifactKeys.CONTENT].strip(), msg="Item {} failed.".format(i))

from data.dataframes.trace_dataframe import TraceKeys
from data.readers.pre_train_trace_reader import PreTrainTraceReader
from testres.base_test import BaseTest

from testres.paths.project_paths import PRE_TRAIN_TRACE_PATH


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
        self.verify_project_data_frames(artifact_df, trace_df, layer_mapping_df)

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

    def verify_project_data_frames(self, artifacts_df, traces_df, layer_df) -> None:
        """
        Verifies dataframes are as expected
        :return: None
        """
        with open(self.get_project_path()) as file:
            expected_artifacts = file.readlines()
        self.assertEquals(len(expected_artifacts), len(artifacts_df.index))
        self.assertEquals(len(traces_df[traces_df[TraceKeys.LABEL] == 1]), len(traces_df[traces_df[TraceKeys.LABEL] == 0]))

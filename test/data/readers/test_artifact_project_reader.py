from unittest import mock

from tgen.data.dataframes.artifact_dataframe import ArtifactKeys
from tgen.data.readers.abstract_project_reader import AbstractProjectReader
from tgen.data.summarizer.summarizer import Summarizer
from tgen.models.llm.open_ai_manager import OpenAIManager
from tgen.testres.base_tests.base_test import BaseTest
from tgen.testres.test_assertions import TestAssertions
from tgen.testres.test_open_ai_responses import SUMMARY_FORMAT, fake_open_ai_completion
from tgen.testres.testprojects.abstract_test_project import AbstractTestProject
from tgen.testres.testprojects.artifact_test_project import ArtifactTestProject
from tgen.train.args.open_ai_args import OpenAIArgs


class TestArtifactProjectReader(BaseTest):
    """
    Tests that artifact project is correctly parsed.
    """
    test_project = ArtifactTestProject()

    def test_read_project(self):
        """
        Tests that the artifact project can be read and translated to artifact data frame.
        """
        self.verify_project_data_frames(self.test_project)

    def test_summarization(self):
        """
        Tests that project artifacts can be summarized
        """
        self.verify_summarization(test_project=self.test_project)

    def verify_project_data_frames(self, test_project: AbstractTestProject) -> None:
        """
        Verifies that entries are found in data frames created by project reader.
        :param test_project: Project containing entities to compare data frames to.
        :return: None
        """
        project_reader = test_project.get_project_reader()
        artifact_df = project_reader.read_project()
        TestAssertions.verify_entities_in_df(self, test_project.get_artifact_entries(), artifact_df)

    @mock.patch("openai.Completion.create", )
    def verify_summarization(self, mock_completion: mock.MagicMock, test_project):
        mock_completion.side_effect = fake_open_ai_completion
        project_reader: AbstractProjectReader = test_project.get_project_reader()
        llm_manager = OpenAIManager(OpenAIArgs())
        project_reader.set_summarizer(Summarizer(llm_manager, code_or_exceeds_limit_only=False))
        artifact_df = project_reader.read_project()
        summary_artifacts = test_project.get_artifact_entries()
        for row in summary_artifacts:
            row[ArtifactKeys.CONTENT.value] = SUMMARY_FORMAT.instructions(row[ArtifactKeys.CONTENT.value])
        TestAssertions.verify_entities_in_df(self, summary_artifacts, artifact_df)

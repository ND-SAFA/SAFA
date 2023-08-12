from tgen.core.args.open_ai_args import OpenAIArgs
from tgen.data.dataframes.artifact_dataframe import ArtifactKeys
from tgen.data.readers.abstract_project_reader import AbstractProjectReader
from tgen.data.summarizer.summarizer import Summarizer
from tgen.models.llm.open_ai_manager import OpenAIManager
from tgen.testres.base_tests.base_test import BaseTest
from tgen.testres.test_assertions import TestAssertions
from tgen.testres.testprojects.artifact_test_project import ArtifactTestProject
from tgen.testres.testprojects.mocking.mock_ai_decorator import mock_openai
from tgen.testres.testprojects.mocking.test_open_ai_responses import SUMMARY_FORMAT
from tgen.testres.testprojects.mocking.test_response_manager import TestAIManager


class TestArtifactProjectReader(BaseTest):
    """
    Tests that artifact project is correctly parsed.
    """
    test_project = ArtifactTestProject()

    def test_read_project(self):
        """
        Tests that the artifact project can be read and translated to artifact data frame.
        """
        project_reader = self.test_project.get_project_reader()
        artifact_df = project_reader.read_project()
        TestAssertions.verify_entities_in_df(self, self.test_project.get_artifact_entries(), artifact_df)

    @mock_openai
    def test_summarization(self, ai_manager: TestAIManager):
        """
        Tests that project artifacts can be summarized
        """
        ai_manager.mock_summarization()
        project_reader: AbstractProjectReader = self.test_project.get_project_reader()
        llm_manager = OpenAIManager(OpenAIArgs())
        project_reader.set_summarizer(Summarizer(llm_manager, code_or_exceeds_limit_only=False))
        artifact_df = project_reader.read_project()
        summary_artifacts = self.test_project.get_artifact_entries()
        for row in summary_artifacts:
            row[ArtifactKeys.CONTENT.value] = SUMMARY_FORMAT.format(row[ArtifactKeys.CONTENT.value])
        TestAssertions.verify_entities_in_df(self, summary_artifacts, artifact_df)

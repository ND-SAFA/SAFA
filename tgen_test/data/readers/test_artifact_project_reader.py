from tgen.data.keys.structure_keys import ArtifactKeys
from tgen.data.readers.abstract_project_reader import AbstractProjectReader
from tgen.data.readers.artifact_project_reader import ArtifactProjectReader
from tgen.summarizer.artifact.artifacts_summarizer import ArtifactsSummarizer
from tgen.testres.base_tests.base_test import BaseTest
from tgen.testres.mocking.mock_anthropic import mock_anthropic
from tgen.testres.mocking.test_open_ai_responses import SUMMARY_FORMAT
from tgen.testres.mocking.test_response_manager import TestAIManager
from tgen.testres.test_assertions import TestAssertions
from tgen.testres.testprojects.artifact_test_project import ArtifactTestProject
from tgen.testres.testprojects.dataframe_test_project import DataFrameTestProject


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

    def test_read_project_from_csv(self):
        """
        Tests that the artifact project can be read and translated to artifact data frame.
        """
        test_project = DataFrameTestProject
        project_path = test_project.get_project_path()
        project_reader = ArtifactProjectReader(project_path)
        artifact_df = project_reader.read_project()
        TestAssertions.verify_entities_in_df(self, test_project.get_artifact_entries(), artifact_df)

    @mock_anthropic
    def test_summarization(self, ai_manager: TestAIManager):
        """
        Tests that project artifacts can be summarized
        """
        ai_manager.mock_summarization()
        project_reader: AbstractProjectReader = self.test_project.get_project_reader()
        project_reader.set_summarizer(ArtifactsSummarizer(summarize_code_only=False))
        artifact_df = project_reader.read_project()
        summary_artifacts = self.test_project.get_artifact_entries()
        for row in summary_artifacts:
            row[ArtifactKeys.SUMMARY.value] = SUMMARY_FORMAT.format(row[ArtifactKeys.CONTENT.value])
        TestAssertions.verify_entities_in_df(self, summary_artifacts, artifact_df)

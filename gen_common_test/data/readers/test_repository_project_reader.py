from gen_common_test.base_tests.abstract_project_reader_test import AbstractProjectReaderTest
from gen_common_test.mocking import mock_anthropic
from gen_common_test.mocking import TestAIManager
from gen_common_test.testprojects.repo_one_test_project import RepositoryOneTestProject


class TestRepositoryProjectReader(AbstractProjectReaderTest):
    """
    Tests that repository reader is able to read project data.
    """

    test_project = RepositoryOneTestProject()

    def test_read_project(self):
        """
        Tests that the repository project can be read and translated to data frames.
        """
        self.verify_project_data_frames(self.test_project)

    @mock_anthropic
    def test_summarization(self, ai_manager: TestAIManager):
        """
        Tests that project artifacts can be summarized
        """
        ai_manager.mock_summarization()
        self.verify_summarization(test_project=self.test_project)

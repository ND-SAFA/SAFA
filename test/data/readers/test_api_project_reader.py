from tgen.testres.base_tests.abstract_project_reader_test import AbstractProjectReaderTest
from tgen.testres.testprojects.api_test_project import ApiTestProject
from tgen.testres.testprojects.mocking.mock_ai_decorator import mock_openai
from tgen.testres.testprojects.mocking.test_response_manager import TestAIManager


class TestClassicProjectReader(AbstractProjectReaderTest):
    """
    Tests that project defines in api can be read into data frames.
    """
    test_project = ApiTestProject()

    def test_read_project(self):
        """
        Tests that the csv project can be read and translated to data frames.
        """
        self.verify_project_data_frames(self.test_project)

    @mock_openai
    def test_summarization(self, ai_manager: TestAIManager):
        """
        Tests that project artifacts can be summarized
        """
        ai_manager.mock_summarization()
        self.verify_summarization(test_project=self.test_project)

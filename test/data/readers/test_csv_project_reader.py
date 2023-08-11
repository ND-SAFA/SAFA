from tgen.testres.base_tests.abstract_project_reader_test import AbstractProjectReaderTest
from tgen.testres.testprojects.csv_test_project import CsvTestProject
from tgen.testres.testprojects.mocking.mock_ai_decorator import mock_openai
from tgen.testres.testprojects.mocking.test_response_manager import TestAIManager


class TestCsvProjectReader(AbstractProjectReaderTest):
    """
    Tests that csv project is correctly parsed.
    """
    test_project = CsvTestProject()

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
        ai_manager.set_responses([self.create_summarization_response] * 12)
        self.verify_summarization(test_project=self.test_project)

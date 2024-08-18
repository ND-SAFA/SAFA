from gen_common_test.base.mock.decorators.mock_anthropic import mock_anthropic
from gen_common_test.base.mock.test_ai_manager import TestAIManager
from gen_common_test.base.tests.abstract_project_reader_test import AbstractProjectReaderTest
from gen_common_test.testprojects.csv_test_project import CsvTestProject


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

    @mock_anthropic
    def test_summarization(self, ai_manager: TestAIManager):
        """
        Tests that project artifacts can be summarized
        """
        ai_manager.mock_summarization()
        self.verify_summarization(test_project=self.test_project)

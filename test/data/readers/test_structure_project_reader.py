from tgen.data.readers.abstract_project_reader import AbstractProjectReader
from tgen.data.readers.structured_project_reader import StructuredProjectReader
from tgen.testres.base_tests.abstract_project_reader_test import AbstractProjectReaderTest
from tgen.testres.paths.project_paths import STRUCTURE_PROJECT_PATH
from tgen.testres.mocking.mock_openai import mock_openai
from tgen.testres.mocking.test_response_manager import TestAIManager
from tgen.testres.testprojects.structured_test_project import StructuredTestProject


class TestStructureProjectReader(AbstractProjectReaderTest):
    """
    Tests that structure project data is read and converted to data frames.
    """
    test_project = StructuredTestProject()

    def test_read_project(self):
        """
        Tests that the repository project can be read and translated to data frames.
        """

        self.verify_project_data_frames(self.test_project)

    @mock_openai
    def test_summarization(self, ai_manager: TestAIManager):
        """
        Tests that project artifacts can be summarized
        """
        ai_manager.mock_summarization()
        self.verify_summarization(test_project=self.test_project)

    def get_project_reader(self) -> AbstractProjectReader:
        return StructuredProjectReader(STRUCTURE_PROJECT_PATH)

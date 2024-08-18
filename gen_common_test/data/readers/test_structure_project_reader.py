from gen_common.data.readers.abstract_project_reader import AbstractProjectReader
from gen_common.data.readers.structured_project_reader import StructuredProjectReader
from gen_common_test.base.mock.decorators.anthropic import mock_anthropic
from gen_common_test.base.mock.test_ai_manager import TestAIManager
from gen_common_test.base.tests.abstract_project_reader_test import AbstractProjectReaderTest
from gen_common_test.paths.project_paths import STRUCTURE_PROJECT_PATH
from gen_common_test.testprojects.structured_test_project import StructuredTestProject


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

    @mock_anthropic
    def test_summarization(self, ai_manager: TestAIManager):
        """
        Tests that project artifacts can be summarized
        """
        ai_manager.mock_summarization()
        self.verify_summarization(test_project=self.test_project)

    def get_project_reader(self) -> AbstractProjectReader:
        return StructuredProjectReader(STRUCTURE_PROJECT_PATH)

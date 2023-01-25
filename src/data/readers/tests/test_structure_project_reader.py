from data.readers.abstract_project_reader import AbstractProjectReader
from data.readers.structured_project_reader import StructuredProjectReader
from data.readers.tests.abstract_project_reader_test import AbstractProjectReaderTest
from testres.paths.project_paths import STRUCTURE_PROJECT_PATH
from testres.testprojects.structured_test_project import StructuredTestProject


class TestStructureProjectReader(AbstractProjectReaderTest):
    """
    Tests that structure project data is read and converted to data frames.
    """

    def test_read_project(self):
        """
        Tests that the repository project can be read and translated to data frames.
        """
        test_project = StructuredTestProject()
        self.verify_project_data_frames(test_project)

    def get_project_reader(self) -> AbstractProjectReader:
        return StructuredProjectReader(STRUCTURE_PROJECT_PATH)

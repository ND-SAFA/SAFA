from tgen.testres.base_tests.abstract_project_reader_test import AbstractProjectReaderTest
from tgen.testres.testprojects.api_test_project import ApiTestProject


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

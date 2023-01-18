from data.datasets.creators.readers.abstract_project_reader import AbstractProjectReader
from data.datasets.creators.readers.api_project_reader import ApiProjectReader
from data.datasets.creators.readers.tests.abstract_project_reader_test import AbstractProjectReaderTest
from testres.test_data_manager import TestDataManager
from testres.testprojects.api_test_project import ApiTestProject


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

    def get_project_reader(self) -> AbstractProjectReader:
        data = {
            "source_layers": TestDataManager.get_path([TestDataManager.Keys.ARTIFACTS, TestDataManager.Keys.SOURCE]),
            "target_layers": TestDataManager.get_path([TestDataManager.Keys.ARTIFACTS, TestDataManager.Keys.TARGET]),
            "true_links": TestDataManager.get_path(TestDataManager.Keys.TRACES)
        }
        return ApiProjectReader(data)

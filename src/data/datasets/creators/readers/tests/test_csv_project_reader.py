from data.datasets.creators.readers.abstract_project_reader import AbstractProjectReader
from data.datasets.creators.readers.csv_project_reader import CsvProjectReader
from data.datasets.creators.readers.tests.abstract_project_reader_test import AbstractProjectReaderTest
from testres.testprojects.csv_test_project import CsvTestProject


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

    def get_project_reader(self) -> AbstractProjectReader:
        return CsvProjectReader(self.test_project.project_path)

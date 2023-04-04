from tgen.data.readers.tests.abstract_project_reader_test import AbstractProjectReaderTest
from test.testres.testprojects.csv_test_project import CsvTestProject


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

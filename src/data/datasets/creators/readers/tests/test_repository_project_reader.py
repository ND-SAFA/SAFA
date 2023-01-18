from data.datasets.creators.readers.abstract_project_reader import AbstractProjectReader
from data.datasets.creators.readers.repository_project_reader import RepositoryProjectReader
from data.datasets.creators.readers.tests.abstract_project_reader_test import AbstractProjectReaderTest
from testres.testprojects.repo_one_test_project import RepositoryOneTestProject


class TestRepositoryProjectReader(AbstractProjectReaderTest):
    """
    Tests that repository reader is able to read project data.
    """

    test_project = RepositoryOneTestProject()

    def test_read_project(self):
        """
        Tests that the repository project can be read and translated to data frames.
        """
        self.verify_project_data_frames(self.test_project)

    def get_project_reader(self) -> AbstractProjectReader:
        return RepositoryProjectReader(self.test_project.project_path)

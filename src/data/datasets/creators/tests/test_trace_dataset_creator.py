from data.datasets.creators.trace_dataset_creator import TraceDatasetCreator
from testres.base_test import BaseTest
from testres.testprojects.abstract_test_project import AbstractTestProject
from testres.testprojects.api_test_project import ApiTestProject
from testres.testprojects.csv_test_project import CsvTestProject
from testres.testprojects.repo_one_test_project import RepositoryOneTestProject
from testres.testprojects.structured_test_project import StructuredTestProject


class TestTraceDatasetCreator(BaseTest):
    """
    Tests that a trace dataset can be created with every type of reader
    """

    def test_csv(self):
        """
        Tests that csv project can be read and converted to trace dataset.
        """
        self.verify_trace_dataset(CsvTestProject())

    def test_api(self):
        """
        Tests that csv project can be read and converted to trace dataset.
        """
        self.verify_trace_dataset(ApiTestProject())

    def test_repo(self):
        """
        Tests that repository project can be read and converted to trace dataset.
        """
        self.verify_trace_dataset(RepositoryOneTestProject())

    def test_structure(self):
        """
        Tests that repository project can be read and converted to trace dataset.
        """
        self.verify_trace_dataset(StructuredTestProject())

    def verify_trace_dataset(self, test_project: AbstractTestProject) -> None:
        """
        Verifies that test project can be converted to trace dataset.
        :param test_project: The test project to be tested.
        :return: None
        """
        project_reader = test_project.get_project_reader()
        trace_dataset_creator = TraceDatasetCreator(project_reader)
        trace_dataset = trace_dataset_creator.create()
        # verify number of links
        self.assertEqual(test_project.get_n_links(), len(trace_dataset))
        # verify number of positive
        n_positive = len(trace_dataset.pos_link_ids)
        self.assertEqual(test_project.get_n_positive_links(), n_positive)

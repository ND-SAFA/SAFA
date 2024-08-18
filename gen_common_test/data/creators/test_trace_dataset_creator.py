from gen_common.data.creators.trace_dataset_creator import TraceDatasetCreator
from gen_common_test.base.tests.base_test import BaseTest
from gen_common_test.testprojects.abstract_test_project import AbstractTestProject
from gen_common_test.testprojects.api_test_project import ApiTestProject
from gen_common_test.testprojects.csv_test_project import CsvTestProject
from gen_common_test.testprojects.dataframe_test_project import DataFrameTestProject
from gen_common_test.testprojects.repo_one_test_project import RepositoryOneTestProject
from gen_common_test.testprojects.safa_test_project import SafaTestProject
from gen_common_test.testprojects.structured_test_project import StructuredTestProject


class TestTraceDatasetCreator(BaseTest):
    """
    Tests that a trace dataset can be created with every type of reader
    """

    def test_csv(self):
        """
        Tests that csv project can be read and converted to trace dataset.
        """
        self.verify_trace_dataset_creation(CsvTestProject(), allowed_orphans=2)

    def test_api(self):
        """
        Tests that project sent via api can be read and converted to trace dataset.
        """
        self.verify_trace_dataset_creation(ApiTestProject(), allowed_orphans=2, remove_orphans=True)

    def test_repo(self):
        """
        Tests that repository can be read and converted to trace dataset.
        """
        self.verify_trace_dataset_creation(RepositoryOneTestProject(), allowed_orphans=1, remove_orphans=True)

    def test_structure(self):
        """
        Tests that structure project can be read and converted to trace dataset.
        """
        self.verify_trace_dataset_creation(StructuredTestProject())

    def test_safa(self):
        """
        Tests that safa project is converted to structured project and converted to trace dataset.
        """
        self.verify_trace_dataset_creation(SafaTestProject())

    def test_dataframe(self):
        """
        Tests that safa project is converted to structured project and converted to trace dataset.
        """
        self.verify_trace_dataset_creation(DataFrameTestProject())

    def verify_trace_dataset_creation(self, test_project: AbstractTestProject, **kwargs) -> None:
        """
        Verifies that test project can be converted to trace dataset.
        :param test_project: The test project to be tested.
        :param kwargs: Additional parameters to construct trace dataset creator.
        :return: None
        """
        project_reader = test_project.get_project_reader()
        trace_dataset_creator = TraceDatasetCreator(project_reader, **kwargs)
        trace_dataset = trace_dataset_creator.create()
        self.assertEqual(test_project.get_n_links(), len(trace_dataset))
        self.assertEqual(test_project.get_n_positive_links(), len(trace_dataset.get_pos_link_ids()))

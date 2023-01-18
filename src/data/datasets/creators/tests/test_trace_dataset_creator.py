from data.datasets.creators.readers.csv_project_reader import CsvProjectReader
from data.datasets.creators.trace_dataset_creator import TraceDatasetCreator
from data.datasets.trace_dataset import TraceDataset
from testres.base_test import BaseTest
from testres.testprojects.abstract_test_project import AbstractTestProject
from testres.testprojects.csv_test_project import CsvTestProject


class TestTraceDatasetCreator(BaseTest):
    """
    Tests that a trace dataset can be created with every type of reader
    """

    def test_create(self):
        test_project = CsvTestProject()
        project_reader = CsvProjectReader(test_project.project_path)
        trace_dataset_creator = TraceDatasetCreator(project_reader)
        trace_dataset = trace_dataset_creator.create()
        self.verify_trace_dataset(test_project, trace_dataset)

    def verify_trace_dataset(self, test_project: AbstractTestProject, trace_dataset: TraceDataset):
        # verify number of links
        self.assertEqual(test_project.get_n_links(), len(trace_dataset))
        # verify number of positive
        n_positive = len(trace_dataset.pos_link_ids)
        self.assertEqual(test_project.get_n_positive_links(), n_positive)

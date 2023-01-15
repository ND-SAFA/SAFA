from data.datasets.creators.abstract_trace_dataset_creator import AbstractTraceDatasetCreator
from data.datasets.creators.readers.entity.csv_entity_reader import CSVEntityReader
from data.datasets.trace_dataset import TraceDataset
from data.processing.cleaning.data_cleaner import DataCleaner


class CSVDatasetCreator(AbstractTraceDatasetCreator):

    def __init__(self, data_file_path: str, data_cleaner: DataCleaner = None):
        """
        Constructs data in CSV format
        :param data_file_path: path to csv
        :param data_cleaner: Responsible for processing artifact tokens.
        """
        super().__init__(data_cleaner, use_linked_targets_only=False)
        self.data_file_path = data_file_path

    def create(self) -> TraceDataset:
        """
        Creates the data from the csv
        :return: the dataset
        """
        project_reader = CSVEntityReader(self.data_file_path)
        trace_links, pos_link_ids, neg_link_ids = project_reader.get_entities()
        return TraceDataset(links=trace_links, pos_link_ids=pos_link_ids, neg_link_ids=neg_link_ids, randomize=True)

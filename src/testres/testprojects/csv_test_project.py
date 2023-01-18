from typing import Dict, List, Tuple

from data.datasets.creators.readers.abstract_project_reader import AbstractProjectReader
from data.datasets.creators.readers.csv_project_reader import CsvProjectReader
from data.datasets.keys.csv_format import CSVKeys
from testres.paths.project_paths import CSV_PROJECT_PATH
from testres.test_data_manager import TestDataManager
from testres.testprojects.abstract_test_project import AbstractTestProject
from testres.testprojects.entry_creator import EntryCreator


class CsvTestProject(AbstractTestProject):
    """
    Contains entries for CSV project. Project is constructed using two batches including
    iterating through 1,2,3 for each source and target. Then, the set 4,5,6 is used in the same manner.
    """

    BATCH_ONE_RANGE = [1, 2, 3]
    BATCH_TWO_RANGE = [4, 5, 6]
    BATCH_RANGES = [BATCH_ONE_RANGE, BATCH_TWO_RANGE]

    @staticmethod
    def get_project_path() -> str:
        """
        :return: Returns path to CSV test project.
        """
        return CSV_PROJECT_PATH

    @classmethod
    def get_project_reader(cls) -> AbstractProjectReader:
        """
        :return: Returns csv reader for project.
        """
        return CsvProjectReader(cls.get_project_path())

    @staticmethod
    def get_source_entries() -> List[List[Dict[str, str]]]:
        """
        :return: Returns list of source artifact entries per layer.
        """
        return EntryCreator.get_entries_in_type(TestDataManager.Keys.SOURCE)

    @staticmethod
    def get_target_entries() -> List[List[Dict[str, str]]]:
        """
        :return: Returns list of target artifact entries per layer.
        """
        return EntryCreator.get_entries_in_type(TestDataManager.Keys.TARGET)

    @classmethod
    def get_trace_entries(cls) -> List[Dict]:
        """
        :return: Returns list of trace entries in project trace data frame..
        """
        trace_data = []
        batch_one, batch_two = cls.get_batch_link_labels()
        labels = batch_one + batch_two
        i = 0
        for batch in cls.BATCH_RANGES:
            for s_id in batch:
                for t_id in batch:
                    trace_data.append((f"s{s_id}", f"t{t_id}", labels[i]))
                    i += 1
        return EntryCreator.create_trace_entries(trace_data)

    @classmethod
    def get_layer_mapping_entries(cls) -> List[Dict]:
        """
        :return: Returns layer mapping entries associated with CSV project.
        """
        return EntryCreator.create_layer_mapping_entries([(CsvProjectReader.get_layer_id(CSVKeys.SOURCE),
                                                           CsvProjectReader.get_layer_id(CSVKeys.TARGET))])

    @staticmethod
    def get_n_links() -> int:
        """
        :return Number of links after removing t3 and s6 which contain no positive links.
        """
        return 12

    @classmethod
    def get_n_positive_links(cls) -> int:
        """
        :return: Returns the number of positive links found in labels.
        """
        n_positive = 0
        for batch in cls.get_batch_link_labels():
            for label in batch:
                n_positive += 1 if label == 1 else 0
        return n_positive

    @classmethod
    def get_csv_entries(cls) -> List[Dict]:
        """
        :return:Returns the CSV entries present in project.
        """
        entries = []
        batch_one_labels, batch_two_labels = cls.get_batch_link_labels()
        entries.extend(CsvTestProject.create_csv_entries([1, 2, 3], [1, 2, 3], batch_one_labels))
        entries.extend(CsvTestProject.create_csv_entries([4, 5, 6], [4, 5, 6], batch_two_labels))

        return entries

    @staticmethod
    def get_batch_link_labels() -> Tuple[List[int], List[int]]:
        """
        :return: Returns the link labels per batch.
        """
        batch_one_labels = [1, 0, 0, 1, 0, 0, 0, 1, 0]
        batch_two_labels = [1, 1, 0, 0, 0, 1, 0, 0, 0]
        return batch_one_labels, batch_two_labels

    @staticmethod
    def create_csv_entries(source_ranges: List[int], target_ranges: List[int], labels: List[int]) -> List[Dict]:
        """
        Returns entities created from ranges.
        :param source_ranges: The indices to iterate for source artifacts.
        :param target_ranges: The indices to iterate for target artifacts.
        :param labels: The labels to use for entries (in order).
        :return: List of entries created.
        """
        if target_ranges is None:
            target_ranges = source_ranges
        entries = []
        i = 0
        for s_index in source_ranges:
            for t_index in target_ranges:
                entries.append({
                    "source_id": f"s{s_index}",
                    "source": f"s_token{s_index}",
                    "target_id": f"t{t_index}",
                    "target": f"t_token{t_index}",
                    "label": labels[i]
                })
                i += 1
        return entries

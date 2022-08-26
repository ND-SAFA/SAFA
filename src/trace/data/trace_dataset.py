import random
from typing import List


class TraceDataset:

    def __init__(self):
        self.data = []
        self.source_target_pairs = []

    def add_entries(self, entries: List[dict], source_target_pairs: List[tuple]) -> None:
        """
        Add the list of entries to the dataset
        :param entries: the list of entries
        :param source_target_pairs: the list of source, target pair ids corresponding to the entries
        :return: None
        """
        for i, entry in enumerate(entries):
            self.add_entry(entry, source_target_pairs[i])

    def add_entry(self, entry: dict, source_target_pair: tuple) -> None:
        """
        Add an individual entry to the dataset
        :param entry: the entry
        :param source_target_pair: source, target pair id corresponding to the entry
        :return: None
        """
        self.data.append(entry)
        self.source_target_pairs.append(source_target_pair)

    @staticmethod
    def resize_data(data: List, new_length: int, include_duplicates: bool = False) -> List:
        """
        Changes the size of the given dataset by using random choice or sample
        :param data: list of data
        :param new_length: desired length
        :param include_duplicates: if True, uses sampling
        :return: a list with the data of the new_length
        """
        include_duplicates = True if new_length > len(data) else include_duplicates  # must include duplicates to make a bigger dataset
        reduction_func = random.choices if include_duplicates else random.sample
        return reduction_func(data, k=new_length)

    @staticmethod
    def resample_data(data: List[dict], resample_rate: int) -> List[dict]:
        """
        Adds multiple copies of each data entry at the given resample rate
        :param data: a list of data entries
        :param resample_rate: the number of copies to make of each entry
        :return: the resampled data
        """
        return [entry for i in range(resample_rate) for entry in data]

    def __len__(self):
        return len(self.data)

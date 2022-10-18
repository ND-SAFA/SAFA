from typing import List


class DataSlice:

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

    def __len__(self):
        return len(self.data)

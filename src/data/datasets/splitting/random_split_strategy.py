from typing import List, Sized

from config.override import overrides
from data.datasets.splitting.abstract_split_strategy import AbstractSplitStrategy
from data.datasets.trace_dataset import TraceDataset


class RandomSplitStrategy(AbstractSplitStrategy):

    @staticmethod
    @overrides(AbstractSplitStrategy)
    def create_split(trace_dataset: TraceDataset, percent_split: float, slice_num: int):
        """
        Creates slice by randomly selecting from all links equally.
        :param trace_dataset: The dataset to split.
        :param percent_split: The percent of the second split.
        :param slice_num: The slice number to retrieve.
        :return: Slice of dataset associated with slice num.
        """
        slice_pos_link_ids = RandomSplitStrategy._get_data_split(trace_dataset.pos_link_ids, percent_split,
                                                                 slice_num == 2)
        slice_neg_link_ids = RandomSplitStrategy._get_data_split(trace_dataset.neg_link_ids, percent_split,
                                                                 slice_num == 2)
        slice_links = {
            link_id: trace_dataset.links[link_id] for link_id in slice_pos_link_ids + slice_neg_link_ids
        }
        return TraceDataset(slice_links)

    @staticmethod
    def _get_data_split(data: List, percent_split: float, for_second_split: bool = False) -> List:
        """
        Splits the data and returns the split
        :param data: a list of the data
        :param percent_split: The percentage of samples in second split.
        :param for_second_split: If True, returns the second portion.
        :return: the subsection of the data in the split
        """
        split_size = RandomSplitStrategy._get_first_split_size(data, percent_split)
        return data[split_size:] if for_second_split else data[:split_size]

    @staticmethod
    def _get_first_split_size(data: Sized, percent_split: float) -> int:
        """
        Gets the size of the data for the first split
        :param data: a list of the data
        :param percent_split: The percentage of samples in second split.
        :return: the size of the data split
        """
        return len(data) - round(len(data) * percent_split)

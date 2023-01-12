from sklearn.model_selection import train_test_split

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

        first_slice_pos_ids, second_slice_pos_ids = train_test_split(trace_dataset.pos_link_ids, test_size=percent_split)
        first_slice_neg_ids, second_slice_neg_ids = train_test_split(trace_dataset.neg_link_ids, test_size=percent_split)
        slice_ids = first_slice_pos_ids + first_slice_neg_ids if slice == 1 else second_slice_pos_ids + second_slice_neg_ids
        slice_links = {link_id: trace_dataset.links[link_id] for link_id in slice_ids}
        return TraceDataset(slice_links)

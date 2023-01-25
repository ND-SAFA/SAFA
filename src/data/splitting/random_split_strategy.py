from config.override import overrides
from data.splitting.abstract_split_strategy import AbstractSplitStrategy
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
        first_slice_pos_ids, second_slice_pos_ids = AbstractSplitStrategy.split_data(trace_dataset.pos_link_ids, percent_split)
        first_slice_neg_ids, second_slice_neg_ids = AbstractSplitStrategy.split_data(trace_dataset.neg_link_ids, percent_split)
        slice_ids = first_slice_pos_ids + first_slice_neg_ids if slice_num == 1 else second_slice_pos_ids + second_slice_neg_ids

        return AbstractSplitStrategy.create_dataset_slice(trace_dataset, slice_ids)

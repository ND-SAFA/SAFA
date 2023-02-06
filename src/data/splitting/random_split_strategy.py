from data.datasets.trace_dataset import TraceDataset
from data.splitting.abstract_trace_split_strategy import AbstractTraceSplitStrategy
from util.override import overrides


class RandomSplitStrategy(AbstractTraceSplitStrategy):

    @staticmethod
    @overrides(AbstractTraceSplitStrategy)
    def create_split(dataset: TraceDataset, percent_split: float, slice_num: int) -> TraceDataset:
        """
        Creates slice by randomly selecting from all links equally.
        :param dataset: The dataset to split.
        :param percent_split: The percent of the second split.
        :param slice_num: The slice number to retrieve.
        :return: Slice of dataset associated with slice num.
        """
        first_slice_pos_ids, second_slice_pos_ids = AbstractTraceSplitStrategy.split_data(dataset.pos_link_ids, percent_split)
        first_slice_neg_ids, second_slice_neg_ids = AbstractTraceSplitStrategy.split_data(dataset.neg_link_ids, percent_split)
        slice_ids = first_slice_pos_ids + first_slice_neg_ids if slice_num == 1 else second_slice_pos_ids + second_slice_neg_ids

        return AbstractTraceSplitStrategy.create_dataset_slice(dataset, slice_ids)

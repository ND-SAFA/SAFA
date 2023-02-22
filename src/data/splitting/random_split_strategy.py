from typing import Tuple

from data.datasets.trace_dataset import TraceDataset
from data.splitting.abstract_trace_split_strategy import AbstractTraceSplitStrategy
from util.override import overrides


class RandomSplitStrategy(AbstractTraceSplitStrategy):

    @overrides(AbstractTraceSplitStrategy)
    def create_split(self, dataset: TraceDataset) -> Tuple[TraceDataset, TraceDataset]:
        """
        Creates slice by randomly selecting from all links equally.
        :param dataset: The dataset to split.
        :return: Slice of dataset associated with slice num.
        """
        first_slice_pos_ids, second_slice_pos_ids = AbstractTraceSplitStrategy.split_data(dataset.pos_link_ids,
                                                                                          self.percent_of_split_dataset)
        first_slice_neg_ids, second_slice_neg_ids = AbstractTraceSplitStrategy.split_data(dataset.neg_link_ids,
                                                                                          self.percent_of_split_dataset)
        slice1 = AbstractTraceSplitStrategy.create_dataset_slice(dataset, first_slice_pos_ids + first_slice_neg_ids)
        slice2 = AbstractTraceSplitStrategy.create_dataset_slice(dataset, second_slice_pos_ids + second_slice_neg_ids)
        return slice1, slice2

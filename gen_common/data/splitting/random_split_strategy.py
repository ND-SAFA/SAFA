from typing import Tuple

from gen_common.data.splitting.abstract_split_strategy import AbstractSplitStrategy
from gen_common.data.splitting.abstract_trace_split_strategy import AbstractTraceSplitStrategy
from gen_common.data.tdatasets.trace_dataset import TraceDataset
from gen_common.util.override import overrides


class RandomSplitStrategy(AbstractTraceSplitStrategy):

    @staticmethod
    @overrides(AbstractSplitStrategy)
    def create_split(dataset: TraceDataset, second_split_percentage: float) -> Tuple[TraceDataset, TraceDataset]:
        """
        Creates the split of the dataset
        :param dataset: The dataset to split.
        :param second_split_percentage: The percentage of the data to be contained in second split
        :return: Dataset containing slice of data.
        """
        first_slice_pos_ids, second_slice_pos_ids = AbstractTraceSplitStrategy.split_data(dataset.get_pos_link_ids(),
                                                                                          second_split_percentage)
        first_slice_neg_ids, second_slice_neg_ids = AbstractTraceSplitStrategy.split_data(dataset.get_neg_link_ids(),
                                                                                          second_split_percentage)
        slice1 = AbstractTraceSplitStrategy.create_dataset_slice(dataset, first_slice_pos_ids + first_slice_neg_ids)
        slice2 = AbstractTraceSplitStrategy.create_dataset_slice(dataset, second_slice_pos_ids + second_slice_neg_ids)
        return slice1, slice2

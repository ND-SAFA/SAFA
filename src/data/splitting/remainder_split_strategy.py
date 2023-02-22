from typing import Tuple, Optional

from data.datasets.trace_dataset import TraceDataset
from data.splitting.abstract_split_strategy import AbstractSplitStrategy
from util.override import overrides


class RemainderSplitStrategy(AbstractSplitStrategy):

    def __init__(self):
        """
        Represents a split that takes the remainder of the dataset
        """
        super().__init__(0)

    @overrides(AbstractSplitStrategy)
    def create_split(self, dataset: TraceDataset) -> Tuple[TraceDataset, Optional[TraceDataset]]:
        """
        Split is just the remainder of the dataset so nothing is done (used for consistency)
        :param dataset: The dataset to split.
        :return: The dataset
        """
        return dataset, None

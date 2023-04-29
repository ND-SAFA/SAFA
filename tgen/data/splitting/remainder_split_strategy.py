from typing import Optional, Tuple

from tgen.data.splitting.abstract_split_strategy import AbstractSplitStrategy
from tgen.data.tdatasets.trace_dataset import TraceDataset
from tgen.util.override import overrides


class RemainderSplitStrategy(AbstractSplitStrategy):

    @staticmethod
    @overrides(AbstractSplitStrategy)
    def create_split(dataset: TraceDataset, second_split_percentage: float) -> Tuple[TraceDataset, Optional[TraceDataset]]:
        """
        Creates the split of the dataset
        :param dataset: The dataset to split.
        :param second_split_percentage: The percentage of the data to be contained in second split
        :return: Dataset containing slice of data.
        """
        return dataset, None

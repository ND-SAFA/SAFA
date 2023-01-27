from typing import List, Tuple, Type, Union

from data.splitting.abstract_split_strategy import AbstractSplitStrategy
from data.splitting.supported_split_strategy import SupportedSplitStrategy
from data.datasets.trace_dataset import TraceDataset


class TraceDatasetSplitter:
    """
    Responsible for splitting a dataset via different strategies.
    """

    def __init__(self, trace_dataset: TraceDataset):
        """
        Creates splitter targetting given dataset.
        :param trace_dataset: The dataset to split.
        """
        self.trace_dataset = trace_dataset

    def split(self, percent_split: float, strategy: str = None):
        """
        Splits trace dataset into two.
        :param percent_split: The percentage of data the second slice should have.
        :param strategy: The split strategies to apply in order to split the data
        :return: Two TraceDatasets
        """
        return self.split_multiple([percent_split], [strategy])

    def split_multiple(self, percent_splits: List[float], strategies: List[str] = None) -> Tuple[TraceDataset]:
        """
         Splits trace data into multiple data, with each part containing the corresponding percentage of links specified.
         :param percent_splits: The percent of links to include trace data for each split.
         :param strategies: The list of split strategies to apply in order to split the data
         :return: Tuple of trace data for each split specified
         """
        if not strategies or strategies[0] is None:
            strategies = [SupportedSplitStrategy.SPLIT_BY_LINK] * len(percent_splits)
        percent_splits = [1 - sum(percent_splits)] + percent_splits
        return self._split_multiple_helper(percent_splits, splits=[self.trace_dataset], strategies=strategies)

    def _split_multiple_helper(self, percent_splits: List, splits: List[TraceDataset], strategies: List[str]) -> Tuple[TraceDataset]:
        """
        Recursive method to split a dataset into multiple parts fir all percentages provided
        :param percent_splits: a list of all split percentages (should sum to 1)
        :param splits: list of already split data (the last element should be the portion remaining to split)
        :return: Tuple of trace data for each split specified
        """
        if len(percent_splits) <= 1:
            return tuple(splits)
        dataset_to_split = splits.pop()
        total_percent_to_split = 1 - percent_splits.pop(0)
        trace_dataset_splitter = TraceDatasetSplitter(dataset_to_split)
        slices = trace_dataset_splitter._create_slices(total_percent_to_split, strategies[0])
        splits.extend(slices)
        updated_percent_splits = [percent_split / total_percent_to_split for percent_split in percent_splits]
        return self._split_multiple_helper(updated_percent_splits, splits, strategies[1:])

    def _create_slices(self, second_percent_split: float, strategy: Union[str, SupportedSplitStrategy]):
        """
        Splits dataset into two with second taking the percentage of links given.
        :param second_percent_split: The percentage of links in second dataset.
        :param strategy: The strategy for creating dataset splits.
        :return: Two TraceDataset containing 1-percent and percent of the trace links.
        """
        if not isinstance(strategy, SupportedSplitStrategy):
            strategy = SupportedSplitStrategy[strategy.upper()]
        split_strategy: Type[AbstractSplitStrategy] = strategy.value
        first_slice = split_strategy.create_split(self.trace_dataset, second_percent_split, slice_num=1)
        second_slice = split_strategy.create_split(self.trace_dataset, second_percent_split, slice_num=2)
        return first_slice, second_slice

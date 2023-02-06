from typing import List, Tuple, Type, Union

from data.datasets.abstract_dataset import AbstractDataset
from data.datasets.pre_train_dataset import PreTrainDataset
from data.splitting.abstract_trace_split_strategy import AbstractTraceSplitStrategy
from data.splitting.supported_split_strategy import SupportedSplitStrategy


class DatasetSplitter:
    """
    Responsible for splitting a dataset via different strategies.
    """

    def __init__(self, dataset: AbstractDataset):
        """
        Creates splitter targetting given dataset.
        :param dataset: The dataset to split.
        """
        self.dataset = dataset

    def split(self, percent_split: float, strategy: str = None):
        """
        Splits the dataset into two.
        :param percent_split: The percentage of data the second slice should have.
        :param strategy: The split strategies to apply in order to split the data
        :return: Two Datasets
        """
        return self.split_multiple([percent_split], [strategy])

    def split_multiple(self, percent_splits: List[float], strategies: List[str] = None) -> Tuple[AbstractDataset]:
        """
         Splits the data into multiple data, with each part containing the corresponding percentage of links specified.
         :param percent_splits: The percent of links to include the data for each split.
         :param strategies: The list of split strategies to apply in order to split the data
         :return: Tuple of the data for each split specified
         """
        if not strategies or strategies[0] is None:
            strategies = [self._get_default_split_strategy()] * len(percent_splits)
        percent_splits = [1 - sum(percent_splits)] + percent_splits
        return self._split_multiple_helper(percent_splits, splits=[self.dataset], strategies=strategies)

    def _get_default_split_strategy(self) -> SupportedSplitStrategy:
        """
        Returns the default split strategy based on the dataset type
        :return: The default split strategy
        """
        if isinstance(self.dataset, PreTrainDataset):
            return SupportedSplitStrategy.PRE_TRAIN
        return SupportedSplitStrategy.SPLIT_BY_LINK

    def _split_multiple_helper(self, percent_splits: List, splits: List[AbstractDataset], strategies: List[str]) \
            -> Tuple[AbstractDataset]:
        """
        Recursive method to split a dataset into multiple parts fir all percentages provided
        :param percent_splits: a list of all split percentages (should sum to 1)
        :param splits: list of already split data (the last element should be the portion remaining to split)
        :return: Tuple of the data for each split specified
        """
        if len(percent_splits) <= 1:
            return tuple(splits)
        dataset_to_split = splits.pop()
        total_percent_to_split = 1 - percent_splits.pop(0)
        dataset_splitter = self.__class__(dataset_to_split)
        slices = dataset_splitter._create_slices(total_percent_to_split, strategies[0])
        splits.extend(slices)
        updated_percent_splits = [percent_split / total_percent_to_split for percent_split in percent_splits]
        return self._split_multiple_helper(updated_percent_splits, splits, strategies[1:])

    def _create_slices(self, second_percent_split: float, strategy: Union[str, SupportedSplitStrategy]):
        """
        Splits dataset into two with second taking the percentage of links given.
        :param second_percent_split: The percentage of links in second dataset.
        :param strategy: The strategy for creating dataset splits.
        :return: Two datasets containing 1-percent and percent of the the links.
        """
        if not isinstance(strategy, SupportedSplitStrategy):
            strategy = SupportedSplitStrategy[strategy.upper()]
        split_strategy: Type[AbstractTraceSplitStrategy] = strategy.value
        first_slice = split_strategy.create_split(self.dataset, second_percent_split, slice_num=1)
        second_slice = split_strategy.create_split(self.dataset, second_percent_split, slice_num=2)
        return first_slice, second_slice

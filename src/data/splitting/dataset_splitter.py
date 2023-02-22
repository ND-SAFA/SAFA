from typing import List, Tuple, Type, Union, Dict

from data.datasets.abstract_dataset import AbstractDataset
from data.datasets.dataset_role import DatasetRole
from data.datasets.pre_train_dataset import PreTrainDataset
from data.splitting.abstract_split_strategy import AbstractSplitStrategy
from data.splitting.abstract_trace_split_strategy import AbstractTraceSplitStrategy
from data.splitting.supported_split_strategy import SupportedSplitStrategy


class DatasetSplitter:
    """
    Responsible for splitting a dataset via different strategies.
    """

    def __init__(self, dataset: AbstractDataset, split_roles_to_strategy: Dict[DatasetRole, AbstractSplitStrategy]):
        """
        Creates splitter targetting given dataset.
        :param dataset: The dataset to split.
        :param split_roles_to_strategy: A dictionary mapping dataset role to the desired split strategy
        """
        self.dataset = dataset
        self.split_roles_to_strategy = split_roles_to_strategy

    def split_dataset(self) -> Dict[DatasetRole, AbstractDataset]:
        percent_splits = [strategy.total_split_percentage for strategy in self.split_roles_to_strategy.values()]
        splits = {}
        percent_rem = 1
        dataset = self.dataset
        i = 0
        for dataset_role, split_strategy in self.split_roles_to_strategy.items():
            split_strategy.update_percent_of_split_dataset(split_strategy.total_split_percentage / percent_rem)
            split1, dataset = split_strategy.create_split(dataset)
            splits[dataset_role] = split1
            i += 1
            percent_rem = sum(percent_splits[i:])
        return splits

    def _get_default_split_strategy(self) -> SupportedSplitStrategy:
        """
        Returns the default split strategy based on the dataset type
        :return: The default split strategy
        """
        if isinstance(self.dataset, PreTrainDataset):
            return SupportedSplitStrategy.PRE_TRAIN
        return SupportedSplitStrategy.SPLIT_BY_LINK

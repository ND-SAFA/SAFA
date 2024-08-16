from typing import Dict, List, OrderedDict

from gen_common.data.splitting.remainder_split_strategy import RemainderSplitStrategy
from gen_common.data.splitting.supported_split_strategy import SupportedSplitStrategy
from gen_common.data.tdatasets.dataset_role import DatasetRole
from gen_common.data.tdatasets.idataset import iDataset
from gen_common.data.tdatasets.pre_train_dataset import PreTrainDataset


class DatasetSplitter:
    """
    Responsible for splitting a dataset via different strategies.
    """

    def __init__(self, dataset: iDataset, dataset_role_to_split_percentage: OrderedDict[DatasetRole, float],
                 strategies: List[SupportedSplitStrategy] = None):
        """
        Creates splitter targeting given dataset.
        :param dataset: The dataset to split.
        :param dataset_role_to_split_percentage: A dictionary mapping dataset role to the desired split percentage
        :param strategies: A list of strategies to apply to obtain each split
        """
        self.dataset = dataset
        self.dataset_role_to_split_percentage = dataset_role_to_split_percentage
        self.strategies = self._get_default_split_strategies() if not strategies else strategies

    def split_dataset(self) -> Dict[DatasetRole, iDataset]:
        """
        Split the dataset based on specifications in split_roles_to_strategy
        :return: A dictionary mapping dataset role to the corresponding split
        """
        splits = {}
        dataset = self.dataset
        percent_already_split = 0
        for i, items in enumerate(self.dataset_role_to_split_percentage.items()):
            dataset_role, total_split_percentage = items
            split_strategy = self.strategies[i].value if i < len(self.strategies) else RemainderSplitStrategy
            percent_to_split = total_split_percentage / (1 - percent_already_split)
            split1, dataset = split_strategy.create_split(dataset, 1 - percent_to_split)
            splits[dataset_role] = split1
            percent_already_split += total_split_percentage
        return splits

    def _get_default_split_strategies(self) -> List[SupportedSplitStrategy]:
        """
        Returns the default split strategy based on the dataset type
        :return: The default split strategy
        """
        default = SupportedSplitStrategy.PRE_TRAIN if isinstance(self.dataset, PreTrainDataset) \
            else SupportedSplitStrategy.SPLIT_BY_LINK
        return [default for i in range(len(self.dataset_role_to_split_percentage.keys()) - 1)]

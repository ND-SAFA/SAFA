from typing import Union

from config.constants import VALIDATION_PERCENTAGE_DEFAULT
from data.datasets.creators.abstract_dataset_creator import AbstractDatasetCreator
from data.datasets.pre_train_dataset import PreTrainDataset
from data.datasets.splitting.supported_split_strategy import SupportedSplitStrategy
from data.datasets.trace_dataset import TraceDataset
from data.processing.cleaning.data_cleaner import DataCleaner


class SplitDatasetCreator(AbstractDatasetCreator):

    def __init__(self, val_percentage: float = VALIDATION_PERCENTAGE_DEFAULT,
                 data_cleaner: DataCleaner = None, split_strategy: str = SupportedSplitStrategy.SOURCE_RANDOM):
        """
        Represents a dataset that is a split of the training dataset
        :param val_percentage: the percent of links to use in this dataset
        """
        if val_percentage > 1:
            raise ValueError("Validation percentage cannot be more than 1.")
        super().__init__(data_cleaner)
        self.val_percentage = val_percentage
        self.split_strategy = split_strategy

    def create(self) -> Union[TraceDataset, PreTrainDataset]:
        """
        Creation will occur by splitting train dataset in Trainer Dataset Container
        :return: None
        """
        return None

from typing import Optional, Union

from tgen.constants import VALIDATION_PERCENTAGE_DEFAULT
from tgen.data.creators.abstract_dataset_creator import AbstractDatasetCreator
from tgen.data.processing.cleaning.data_cleaner import DataCleaner
from tgen.data.splitting.supported_split_strategy import SupportedSplitStrategy
from tgen.data.tdatasets.pre_train_dataset import PreTrainDataset
from tgen.data.tdatasets.trace_dataset import TraceDataset


class SplitDatasetCreator(AbstractDatasetCreator):

    def __init__(self, val_percentage: float = VALIDATION_PERCENTAGE_DEFAULT,
                 data_cleaner: DataCleaner = None, split_strategy: str = SupportedSplitStrategy.SPLIT_BY_SOURCE):
        """
        Represents a dataset that is a split of the training dataset
        :param val_percentage: the percent of links to use in this dataset
        """
        if val_percentage > 1:
            raise ValueError("Validation percentage cannot be more than 1.")
        super().__init__(data_cleaner)
        self.val_percentage = val_percentage
        self.split_strategy = split_strategy
        self.name = ''

    def create(self) -> Optional[Union[TraceDataset, PreTrainDataset]]:
        """
        Creation will occur by splitting train dataset in Trainer Dataset Container
        :return: None
        """
        return None

    def get_name(self) -> str:
        """
        Returns the name of the dataset which was split, if set else empty string
        :return: the name of the dataset which was split, if set else empty string
        """
        return self.name

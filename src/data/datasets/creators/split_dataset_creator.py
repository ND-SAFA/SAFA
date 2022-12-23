from typing import Union

from config.constants import VALIDATION_PERCENTAGE_DEFAULT
from data.datasets.creators.abstract_dataset_creator import AbstractDatasetCreator
from data.datasets.pre_train_dataset import PreTrainDataset
from data.datasets.trace_dataset import TraceDataset


class SplitDatasetCreator(AbstractDatasetCreator):

    def __init__(self, split_percentage: float = VALIDATION_PERCENTAGE_DEFAULT):
        """
        Represents a dataset that is a split of the training dataset
        :param split_percentage: the percent of links to use in this dataset
        """
        super().__init__([])
        self.split_percentage = split_percentage

    def create(self) -> Union[TraceDataset, PreTrainDataset]:
        """
        Creation will occur by splitting train dataset in Trainer Dataset Container
        :return: None
        """
        return None

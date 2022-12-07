from typing import List, Union

from config.constants import VALIDATION_PERCENTAGE_DEFAULT
from data.creators.abstract_dataset_creator import AbstractDatasetCreator
from data.datasets.pre_train_dataset import PreTrainDataset
from data.datasets.trace_dataset import TraceDataset
from data.processing.abstract_data_processing_step import AbstractDataProcessingStep


class SplitDatasetCreator(AbstractDatasetCreator):

    def __init__(self, val_percentage: float = VALIDATION_PERCENTAGE_DEFAULT,
                 data_cleaning_steps: List[AbstractDataProcessingStep] = None):
        """
        Represents a dataset that is a split of the training dataset
        :param val_percentage: the percent of links to use in this dataset
        """
        if val_percentage > 1:
            raise ValueError("Validation percentage cannot be more than 1.")
        super().__init__(data_cleaning_steps)
        self.val_percentage = val_percentage

    def create(self) -> Union[TraceDataset, PreTrainDataset]:
        """
        Creation will occur by splitting train dataset in Trainer Dataset Container
        :return: None
        """
        return None

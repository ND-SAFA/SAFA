from enum import Enum

from data.datasets.creators.mlm_pre_train_dataset_creator import MLMPreTrainDatasetCreator
from data.datasets.creators.split_dataset_creator import SplitDatasetCreator
from data.datasets.creators.trace_dataset_creator import TraceDatasetCreator


class SupportedDatasetCreator(Enum):
    PRETRAIN = MLMPreTrainDatasetCreator
    SPLIT = SplitDatasetCreator
    TRACE = TraceDatasetCreator

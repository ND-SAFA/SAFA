from enum import Enum

from data.creators.mlm_pre_train_dataset_creator import MLMPreTrainDatasetCreator
from data.creators.split_dataset_creator import SplitDatasetCreator
from data.creators.trace_dataset_creator import TraceDatasetCreator


class SupportedDatasetCreator(Enum):
    MLM_PRETRAIN = MLMPreTrainDatasetCreator
    SPLIT = SplitDatasetCreator
    TRACE = TraceDatasetCreator

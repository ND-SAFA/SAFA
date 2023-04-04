from enum import Enum

from tgen.data.creators.mlm_pre_train_dataset_creator import MLMPreTrainDatasetCreator
from tgen.data.creators.multi_trace_dataset_creator import MultiTraceDatasetCreator
from tgen.data.creators.split_dataset_creator import SplitDatasetCreator
from tgen.data.creators.trace_dataset_creator import TraceDatasetCreator


class SupportedDatasetCreator(Enum):
    MLM_PRE_TRAIN = MLMPreTrainDatasetCreator
    SPLIT = SplitDatasetCreator
    TRACE = TraceDatasetCreator
    MULTI = MultiTraceDatasetCreator

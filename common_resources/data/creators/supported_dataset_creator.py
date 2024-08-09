from enum import Enum

from common_resources.data.creators.mlm_pre_train_dataset_creator import MLMPreTrainDatasetCreator
from common_resources.data.creators.multi_trace_dataset_creator import MultiTraceDatasetCreator
from common_resources.data.creators.prompt_dataset_creator import PromptDatasetCreator
from common_resources.data.creators.split_dataset_creator import SplitDatasetCreator
from common_resources.data.creators.trace_dataset_creator import TraceDatasetCreator


class SupportedDatasetCreator(Enum):
    MLM_PRE_TRAIN = MLMPreTrainDatasetCreator
    SPLIT = SplitDatasetCreator
    TRACE = TraceDatasetCreator
    MULTI = MultiTraceDatasetCreator
    PROMPT = PromptDatasetCreator

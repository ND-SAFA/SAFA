from enum import Enum

from gen_common.data.creators.mlm_pre_train_dataset_creator import MLMPreTrainDatasetCreator
from gen_common.data.creators.multi_trace_dataset_creator import MultiTraceDatasetCreator
from gen_common.data.creators.prompt_dataset_creator import PromptDatasetCreator
from gen_common.data.creators.split_dataset_creator import SplitDatasetCreator
from gen_common.data.creators.trace_dataset_creator import TraceDatasetCreator


class SupportedDatasetCreator(Enum):
    MLM_PRE_TRAIN = MLMPreTrainDatasetCreator
    SPLIT = SplitDatasetCreator
    TRACE = TraceDatasetCreator
    MULTI = MultiTraceDatasetCreator
    PROMPT = PromptDatasetCreator

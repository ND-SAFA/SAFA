from enum import Enum

from tracer.dataset.creators.csv_dataset_creator import CSVDatasetCreator
from tracer.dataset.creators.mlm_pre_train_dataset_creator import MLMPreTrainDatasetCreator
from tracer.dataset.creators.safa_dataset_creator import SafaDatasetCreator
from tracer.dataset.creators.classic_trace_dataset_creator import ClassicTraceDatasetCreator


class SupportedDatasetCreator(Enum):
    CSV = CSVDatasetCreator
    SAFA = SafaDatasetCreator
    CLASSIC_TRACE = ClassicTraceDatasetCreator
    MLM_PRETRAIN = MLMPreTrainDatasetCreator

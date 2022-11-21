from enum import Enum

from tracer.datasets.creators.classic_trace_dataset_creator import ClassicTraceDatasetCreator
from tracer.datasets.creators.csv_dataset_creator import CSVDatasetCreator
from tracer.datasets.creators.mlm_pre_train_dataset_creator import MLMPreTrainDatasetCreator
from tracer.datasets.creators.safa_dataset_creator import SafaDatasetCreator


class SupportedDatasetCreator(Enum):
    CSV = CSVDatasetCreator
    SAFA = SafaDatasetCreator
    CLASSIC_TRACE = ClassicTraceDatasetCreator
    MLM_PRETRAIN = MLMPreTrainDatasetCreator

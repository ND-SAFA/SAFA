from enum import Enum

from data.datasets.creators.classic_trace_dataset_creator import ClassicTraceDatasetCreator
from data.datasets.creators.csv_dataset_creator import CSVDatasetCreator
from data.datasets.creators.mlm_pre_train_dataset_creator import MLMPreTrainDatasetCreator
from data.datasets.creators.safa_dataset_creator import SafaDatasetCreator


class SupportedDatasetCreator(Enum):
    CSV = CSVDatasetCreator
    SAFA = SafaDatasetCreator
    CLASSIC_TRACE = ClassicTraceDatasetCreator
    MLM_PRETRAIN = MLMPreTrainDatasetCreator

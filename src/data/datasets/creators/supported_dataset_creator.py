from enum import Enum

from data.datasets.creators.classic_trace_dataset_creator import ClassicTraceDatasetCreator
from data.datasets.creators.csv_dataset_creator import CSVDatasetCreator
from data.datasets.creators.mlm_pre_train_dataset_creator import MLMPreTrainDatasetCreator
from data.datasets.creators.safa_dataset_creator import SafaDatasetCreator
from data.datasets.creators.split_dataset_creator import SplitDatasetCreator
from data.datasets.creators.structure_dataset_creator import StructureDatasetCreator


class SupportedDatasetCreator(Enum):
    STRUCTURE = StructureDatasetCreator
    CSV = CSVDatasetCreator
    SAFA = SafaDatasetCreator
    CLASSIC_TRACE = ClassicTraceDatasetCreator
    MLM_PRETRAIN = MLMPreTrainDatasetCreator
    SPLIT = SplitDatasetCreator

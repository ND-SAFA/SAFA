from enum import Enum

from tracer.dataset.creators.csv_dataset_creator import CSVDatasetCreator
from tracer.dataset.creators.safa_dataset_creator import SafaDatasetCreator
from tracer.dataset.creators.trace_dataset_creator import TraceDatasetCreator


class SupportedDatasetCreator(Enum):
    CSV = CSVDatasetCreator
    SAFA = SafaDatasetCreator
    TRACE = TraceDatasetCreator

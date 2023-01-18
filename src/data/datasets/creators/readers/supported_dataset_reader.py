from enum import Enum

from data.datasets.creators.readers.api_project_reader import ApiProjectReader
from data.datasets.creators.readers.csv_project_reader import CsvProjectReader
from data.datasets.creators.readers.pre_train_project_reader import PreTrainProjectReader
from data.datasets.creators.readers.repository_project_reader import RepositoryProjectReader
from data.datasets.creators.readers.structured_project_reader import StructuredProjectReader


class SupportedDatasetReader(Enum):
    STRUCTURE = StructuredProjectReader
    REPOSITORY = RepositoryProjectReader
    CSV = CsvProjectReader
    SAFA = StructuredProjectReader
    CLASSIC_TRACE = ApiProjectReader
    MLM_PRETRAIN = PreTrainProjectReader

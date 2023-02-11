from enum import Enum

from data.readers.api_project_reader import ApiProjectReader
from data.readers.csv_project_reader import CsvProjectReader
from data.readers.hub_project_reader import HubProjectReader
from data.readers.pre_train_project_reader import PreTrainProjectReader
from data.readers.repository_project_reader import RepositoryProjectReader
from data.readers.structured_project_reader import StructuredProjectReader


class SupportedDatasetReader(Enum):
    STRUCTURE = StructuredProjectReader
    REPOSITORY = RepositoryProjectReader
    CSV = CsvProjectReader
    SAFA = StructuredProjectReader
    API = ApiProjectReader
    MLM_PRETRAIN = PreTrainProjectReader
    HUB = HubProjectReader

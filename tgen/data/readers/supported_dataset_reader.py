from enum import Enum

from tgen.data.readers.api_project_reader import ApiProjectReader
from tgen.data.readers.artifact_project_reader import ArtifactProjectReader
from tgen.data.readers.csv_project_reader import CsvProjectReader
from tgen.data.readers.dataframe_project_reader import DataFrameProjectReader
from tgen.data.readers.hub_project_reader import HubProjectReader
from tgen.data.readers.pre_train_project_reader import PreTrainProjectReader
from tgen.data.readers.pre_train_trace_reader import PreTrainTraceReader
from tgen.data.readers.repository_project_reader import RepositoryProjectReader
from tgen.data.readers.structured_project_reader import StructuredProjectReader


class SupportedDatasetReader(Enum):
    ARTIFACT = ArtifactProjectReader
    DATAFRAME = DataFrameProjectReader
    STRUCTURE = StructuredProjectReader
    REPOSITORY = RepositoryProjectReader
    CSV = CsvProjectReader
    SAFA = StructuredProjectReader
    API = ApiProjectReader
    MLM_PRETRAIN = PreTrainProjectReader
    PRE_TRAIN_TRACE = PreTrainTraceReader
    HUB = HubProjectReader

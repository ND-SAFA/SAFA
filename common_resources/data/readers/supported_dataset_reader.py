from common_resources.tools.util.supported_enum import SupportedEnum
from common_resources.data.readers.api_project_reader import ApiProjectReader
from common_resources.data.readers.artifact_project_reader import ArtifactProjectReader
from common_resources.data.readers.csv_project_reader import CsvProjectReader
from common_resources.data.readers.dataframe_project_reader import DataFrameProjectReader
from common_resources.data.readers.hub_project_reader import HubProjectReader
from common_resources.data.readers.pre_train_project_reader import PreTrainProjectReader
from common_resources.data.readers.pre_train_trace_reader import PreTrainTraceReader
from common_resources.data.readers.repository_project_reader import RepositoryProjectReader
from common_resources.data.readers.structured_project_reader import StructuredProjectReader


class SupportedDatasetReader(SupportedEnum):
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

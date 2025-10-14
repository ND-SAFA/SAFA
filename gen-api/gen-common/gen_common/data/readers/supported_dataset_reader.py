from gen_common.data.readers.api_project_reader import ApiProjectReader
from gen_common.data.readers.artifact_project_reader import ArtifactProjectReader
from gen_common.data.readers.csv_project_reader import CsvProjectReader
from gen_common.data.readers.dataframe_project_reader import DataFrameProjectReader
from gen_common.data.readers.hub_project_reader import HubProjectReader
from gen_common.data.readers.pre_train_project_reader import PreTrainProjectReader
from gen_common.data.readers.pre_train_trace_reader import PreTrainTraceReader
from gen_common.data.readers.repository_project_reader import RepositoryProjectReader
from gen_common.data.readers.structured_project_reader import StructuredProjectReader
from gen_common.util.supported_enum import SupportedEnum


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

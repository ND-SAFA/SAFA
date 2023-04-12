from tgen.jobs.create_datasets_job import CreateDatasetsJob
from tgen.jobs.create_model_job import CreateModelJob
from tgen.jobs.create_source_splits_job import CreateSourceSplitsJob
from tgen.jobs.delete_model_job import DeleteModelJob
from tgen.jobs.download_repository_job import DownloadRepositoryJob
from tgen.jobs.export_artifacts_job import ExportArtifactsJob
from tgen.jobs.mlm_pre_train_job import MLMPreTrainJob
from tgen.jobs.open_ai_job import OpenAIJob
from tgen.jobs.predict_job import PredictJob
from tgen.jobs.push_model_job import PushModelJob
from tgen.jobs.train_job import TrainJob
from tgen.jobs.vsm_job import VSMJob
from tgen.util.supported_enum import SupportedEnum


class SupportedJobType(SupportedEnum):
    EXPORT_ARTIFACTS = ExportArtifactsJob
    PUSH_MODEL = PushModelJob
    CREATE_DATASETS = CreateDatasetsJob
    CREATE_MODEL = CreateModelJob
    DELETE_MODEL = DeleteModelJob
    MLM_PRE_TRAIN = MLMPreTrainJob
    OPEN_AI = OpenAIJob
    PRE_TRAIN = MLMPreTrainJob
    PREDICT = PredictJob
    TRAIN = TrainJob
    VSM = VSMJob
    DOWNLOAD_REPO = DownloadRepositoryJob
    CREATE_SOURCE_SPLITS = CreateSourceSplitsJob

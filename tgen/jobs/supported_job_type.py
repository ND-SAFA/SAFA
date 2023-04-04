from enum import Enum

from jobs.create_datasets_job import CreateDatasetsJob
from jobs.create_model_job import CreateModelJob
from jobs.create_source_splits_job import CreateSourceSplitsJob
from jobs.delete_model_job import DeleteModelJob
from jobs.download_repository_job import DownloadRepositoryJob
from jobs.export_artifacts_job import ExportArtifactsJob
from jobs.mlm_pre_train_job import MLMPreTrainJob
from jobs.open_ai_job import OpenAIJob
from jobs.predict_job import PredictJob
from jobs.push_model_job import PushModelJob
from jobs.train_job import TrainJob
from jobs.vsm_job import VSMJob


class SupportedJobType(Enum):
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

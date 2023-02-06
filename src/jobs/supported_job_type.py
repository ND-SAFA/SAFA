from enum import Enum

from jobs.create_datasets_job import CreateDatasetsJob
from jobs.create_model_job import CreateModelJob
from jobs.delete_model_job import DeleteModelJob
from jobs.export_artifacts_job import ExportArtifactsJob
from jobs.gan_train_job import GanTrainJob
from jobs.mlm_pre_train_job import MLMPreTrainJob
from jobs.predict_job import PredictJob
from jobs.push_model_job import PushModelJob
from jobs.train_job import TrainJob


class SupportedJobType(Enum):
    EXPORT_ARTIFACTS = ExportArtifactsJob
    PUSH_MODEL = PushModelJob
    CREATE_DATASETS = CreateDatasetsJob
    CREATE_MODEL = CreateModelJob
    DELETE_MODEL = DeleteModelJob
    GAN_TRAIN = GanTrainJob
    MLM_PRE_TRAIN = MLMPreTrainJob
    PRE_TRAIN = MLMPreTrainJob
    PREDICT = PredictJob
    TRAIN = TrainJob

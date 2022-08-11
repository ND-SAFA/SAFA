from enum import Enum

from pretrain.jobs.build_pretrain_data_job import BuildPretrainDataJob
from pretrain.jobs.pretrain_job import PretrainJob
from trace.jobs.predict_job import PredictJob
from trace.jobs.train_job import TrainJob


class JobType(Enum):
    PRETRAIN = PretrainJob
    TRAIN = TrainJob
    BUILD_PRETRAIN_DATA = BuildPretrainDataJob
    PREDICT = PredictJob

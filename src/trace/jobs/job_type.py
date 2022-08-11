from enum import Enum

from jobs.pretrain.build_pretrain_data_job import BuildPretrainDataJob
from jobs.pretrain.pretrain_job import PretrainJob
from jobs.trace.predict_job import PredictJob
from jobs.trace.train_job import TrainJob


class JobType(Enum):
    PRETRAIN = PretrainJob
    TRAIN = TrainJob
    BUILD_PRETRAIN_DATA = BuildPretrainDataJob
    PREDICT = PredictJob

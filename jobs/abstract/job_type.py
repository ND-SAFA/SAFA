from enum import Enum
from jobs.fine_tune.predict_job import PredictJob
from jobs.fine_tune.train_job import TrainJob
from jobs.pretrain.pretrain_job import PretrainJob
from jobs.pretrain.build_pretrain_data_job import BuildPretrainDataJob


class JobType(Enum):
    PRETRAIN = PretrainJob
    TRAIN = TrainJob
    BUILD_PRETRAIN_DATA = BuildPretrainDataJob
    PREDICT = PredictJob

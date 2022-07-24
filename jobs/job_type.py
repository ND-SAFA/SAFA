from enum import IntEnum, auto
from jobs.pretrain_job import PretrainJob
from jobs.train_job import TrainJob
from jobs.predict_job import PredictJob


class JobType(IntEnum):
    PRETRAIN = auto()
    TRAIN = auto()
    EVALUATE = auto()


JOBS = {JobType.PRETRAIN: PretrainJob,
        JobType.TRAIN: TrainJob,
        JobType.EVALUATE: PredictJob}

from enum import Enum

from experiment.jobs.experiment_job import ExperimentJob
from experiment.jobs.pre_train_job import MLMPreTrainJob
from jobs.create_model_job import CreateModelJob
from jobs.delete_model_job import DeleteModelJob
from jobs.predict_job import PredictJob
from jobs.train_job import TrainJob


class JobType(Enum):
    PRETRAIN = MLMPreTrainJob
    TRAIN = TrainJob
    PREDICT = PredictJob
    CREATE_MODEL = CreateModelJob
    DELETE_MODEL = DeleteModelJob
    EXPERIMENT = ExperimentJob

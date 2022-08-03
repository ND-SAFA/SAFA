from jobs.abstract.job_type import JobType
from jobs.fine_tune.predict_job import PredictJob
from jobs.pretrain.abstract_pretrain_job import AbstractPreTrainJob
from jobs.fine_tune.train_job import TrainJob

JOBS = {JobType.PRETRAIN: AbstractPreTrainJob,
        JobType.TRAIN: TrainJob,
        JobType.EVALUATE: PredictJob}

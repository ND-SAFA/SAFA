from jobs.base_job import BaseJob
from train.trainer import LMTrainer


class EvaluateJob(BaseJob):
    def _start(self, trainer: LMTrainer):
        trainer.predict()

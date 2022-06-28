from jobs.base_job import BaseJob
from train.trainer import LMTrainer


class TrainJob(BaseJob):

    def _get_checkpoint(self) -> str:
        pass

    def _start(self, trainer: LMTrainer):
        checkpoint = self._get_checkpoint()
        results = trainer.train(checkpoint=checkpoint)
        trainer.save(results)

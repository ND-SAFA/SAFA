from jobs.base_job import BaseJob


class TrainJob(BaseJob):

    def _get_checkpoint(self) -> str:
        pass

    def _start(self):
        checkpoint = self._get_checkpoint()
        trainer = self._get_trainer()
        results = trainer.train(checkpoint=checkpoint)
        results.save()

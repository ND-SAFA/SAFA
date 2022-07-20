from jobs.base_job import BaseJob


class EvaluateJob(BaseJob):
    def __start(self):
        trainer = self._get_trainer()
        results = trainer.perform_prediction()
        results.save()


from jobs.base_job import BaseJob


class PredictJob(BaseJob):
    def __start(self):
        trainer = self._get_trainer()
        results = trainer.perform_prediction()
        if self.args.metrics:
            results.evaluate(self.args.metrics)


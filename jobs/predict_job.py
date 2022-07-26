from jobs.base_job import BaseLMJob


class PredictJob(BaseLMJob):
    def __start(self):
        results = self.trainer.perform_prediction()
        if self.args.metrics:
            results.evaluate(self.args.metrics)

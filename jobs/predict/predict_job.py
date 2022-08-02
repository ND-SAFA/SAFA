from jobs.abstract.abstract_model_job import AbstractModelJob
from jobs.abstract.job_result import JobResult


class PredictJob(AbstractModelJob):

    def __start(self) -> JobResult:
        """
        Performs predictions and (optionally) evaluation of model
        :return: result of prediction including predictions, metrics (if evaluating), etc.
        """
        output = self.trainer.perform_prediction()
        return JobResult(output)

from jobs.base_job import BaseLMJob
from jobs.job_result import JobResult


class PredictJob(BaseLMJob):

    def __start(self) -> JobResult:
        """
        Performs predictions and (optionally) evaluation of model
        :return: result of prediction including predictions, metrics (if evaluating), etc.
        """
        output = self.trainer.perform_prediction()
        return JobResult(output)

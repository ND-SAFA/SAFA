from jobs.fine_tune.abstract_fine_tune_job import AbstractFineTuneJob
from jobs.abstract.job_result import JobResult


class PredictJob(AbstractFineTuneJob):

    def __start(self) -> JobResult:
        """
        Performs predictions and (optionally) evaluation of model
        :return: result of prediction including predictions, metrics (if evaluating), etc.
        """
        output = self.trainer.perform_prediction()
        return JobResult(output)

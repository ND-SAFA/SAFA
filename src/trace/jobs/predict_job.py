from common.jobs.job_result import JobResult
from trace.jobs.abstract_trace_job import AbstractTraceJob


class PredictJob(AbstractTraceJob):

    def start(self) -> JobResult:
        """
        Performs predictions and (optionally) evaluation of model
        :return: result of prediction including predictions, metrics (if evaluating), etc.
        """
        output = self.trainer.perform_prediction()
        return JobResult(output)

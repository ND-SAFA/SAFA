from jobs.common.job_result import JobResult
from jobs.trace.abstract_trace_job import AbstractTraceJob


class PredictJob(AbstractTraceJob):

    def __start(self) -> JobResult:
        """
        Performs predictions and (optionally) evaluation of model
        :return: result of prediction including predictions, metrics (if evaluating), etc.
        """
        output = self.trainer.perform_prediction()
        return JobResult(output)

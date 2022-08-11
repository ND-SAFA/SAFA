from jobs.common.job_result import JobResult
from jobs.trace.abstract_trace_job import AbstractTraceJob


class TrainJob(AbstractTraceJob):

    def __start(self) -> JobResult:
        """
        Runs the training and obtains results
        :return: the results of the training
        """
        output = self.trainer.perform_training()
        return JobResult(output)

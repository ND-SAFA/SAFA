from jobs.base_job import BasePretrainJob
from jobs.job_result import JobResult


class PretrainJob(BasePretrainJob):

    def __start(self) -> JobResult:
        """
        Runs the pretraining
        :return: the results of the pretraining
        """
        self.pretrain.train()
        return JobResult()

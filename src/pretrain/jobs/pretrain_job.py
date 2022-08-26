from common.jobs.job_result import JobResult
from pretrain.jobs.abstract_pretrain_job import AbstractPreTrainJob


class PretrainJob(AbstractPreTrainJob):

    def start(self) -> JobResult:
        """
        Runs the pretraining
        :return: the results of the pretraining
        """
        self.pretrainer.train()
        return JobResult()

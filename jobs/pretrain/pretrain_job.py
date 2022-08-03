from jobs.abstract.job_result import JobResult
from jobs.pretrain.abstract_pretrain_job import AbstractPreTrainJob


class PretrainJob(AbstractPreTrainJob):

    def __start(self) -> JobResult:
        """
        Runs the pretraining
        :return: the results of the pretraining
        """
        self.pretrain.train()
        return JobResult()

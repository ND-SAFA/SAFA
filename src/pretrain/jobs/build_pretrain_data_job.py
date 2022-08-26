from common.jobs.job_result import JobResult
from pretrain.jobs.abstract_pretrain_job import AbstractPreTrainJob


class BuildPretrainDataJob(AbstractPreTrainJob):

    def start(self) -> JobResult:
        """
        Runs the dataset building for pretraining
        :return: the results of the data build
        """
        self.pretrainer.build_pretraining_data()
        return JobResult()

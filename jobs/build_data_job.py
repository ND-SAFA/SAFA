from jobs.base_job import BasePretrainJob
from jobs.job_result import JobResult


class BuildPretrainDataJob(BasePretrainJob):

    def __start(self) -> JobResult:
        """
        Runs the dataset building for pretraining
        :return: the results of the data build
        """
        self.pretrain.build_pretraining_data()
        return JobResult()

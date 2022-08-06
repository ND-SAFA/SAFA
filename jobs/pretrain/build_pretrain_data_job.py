from jobs.common.job_result import JobResult
from jobs.pretrain.abstract_pretrain_job import AbstractPreTrainJob


class BuildPretrainDataJob(AbstractPreTrainJob):

    def __start(self) -> JobResult:
        """
        Runs the dataset building for pretraining
        :return: the results of the data build
        """
        self.pretrain.build_pretraining_data()
        return JobResult()

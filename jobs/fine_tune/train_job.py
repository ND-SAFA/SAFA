from jobs.fine_tune.abstract_fine_tune_job import AbstractFineTuneJob
from jobs.abstract.job_result import JobResult


class TrainJob(AbstractFineTuneJob):

    def __start(self) -> JobResult:
        """
        Runs the training and obtains results
        :return: the results of the training
        """
        output = self.trainer.perform_training()
        return JobResult(output)

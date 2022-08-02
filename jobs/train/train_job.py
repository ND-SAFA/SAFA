from jobs.abstract.abstract_model_job import AbstractModelJob
from jobs.abstract.job_result import JobResult


class TrainJob(AbstractModelJob):

    # TODO
    def _get_checkpoint(self) -> str:
        """
        Gets the current checkpoint file path
        :return: the checkpoint file path
        """
        pass

    def __start(self) -> JobResult:
        """
        Runs the training and obtains results
        :return: the results of the training
        """
        checkpoint = self._get_checkpoint()
        output = self.trainer.perform_training(checkpoint=checkpoint)
        return JobResult(output)

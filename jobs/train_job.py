from jobs.base_job import BaseLMJob


class TrainJob(BaseLMJob):

    def _get_checkpoint(self) -> str:
        pass

    def __start(self):
        checkpoint = self._get_checkpoint()
        results = self.trainer.perform_training(checkpoint=checkpoint)



from jobs.train_job import TrainJob
from train.gan.gan_trainer import GanTrainer


class GanTrainJob(TrainJob):
    """
    Job to train a GAN-BERT for trace prediction.
    """

    def get_trainer(self, **kwargs) -> GanTrainer:
        """
        Gets the trace trainer for the job
        :return: the trainer
        """
        if self._trainer is None:
            self._trainer = GanTrainer(args=self.trainer_args, model_manager=self.model_manager,
                                       trainer_dataset_manager=self.trainer_dataset_manager, **kwargs)
        return self._trainer

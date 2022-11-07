from transformers import AutoModel

from jobs.train_job import TrainJob
from tracer.train.gan.gan_trainer import GanTrainer


class GanTrainJob(TrainJob):

    def get_trainer(self, **kwargs) -> GanTrainer:
        """
        Gets the trace trainer for the job
        :param kwargs: any additional parameters for the trainer
        :return: the trainer
        """
        if self._trainer is None:
            model_generator = self.get_model_generator()
            model_generator.base_model_class = AutoModel
            self._trainer = GanTrainer(args=self.train_args, model_generator=model_generator, **kwargs)
        return self._trainer

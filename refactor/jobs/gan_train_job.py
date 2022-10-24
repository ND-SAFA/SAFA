from jobs.train_job import TrainJob
from tracer.train.gan_trainer import GanTrainer


class GanTrainJob(TrainJob):

    def get_trainer(self, **kwargs) -> GanTrainer:
        """
        Gets the trace trainer for the job
        :param kwargs: any additional parameters for the trainer
        :return: the trainer
        """
        if self.__trainer is None:
            self.__trainer = GanTrainer(args=self.train_args, model_generator=self.model_generator, **kwargs)
        return self.__trainer

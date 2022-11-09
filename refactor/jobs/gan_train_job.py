from jobs.job_args import JobArgs
from jobs.train_job import TrainJob
from tracer.models.base_models.supported_base_model import SupportedBaseModel
from tracer.train.gan.gan_trainer import GanTrainer


class GanTrainJob(TrainJob):
    """
    Job to train a GAN-BERT for trace prediction.
    """

    def __init__(self, job_args: JobArgs):
        job_args.base_model = SupportedBaseModel.AUTO_MODEL
        super().__init__(job_args)

    def get_trainer(self) -> GanTrainer:
        """
        Gets the trace trainer for the job
        :param kwargs: any additional parameters for the trainer
        :return: the trainer
        """
        if self._trainer is None:
            self._trainer = GanTrainer(args=self.train_args, model_generator=self.get_model_generator())
        return self._trainer

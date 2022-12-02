from jobs.components.job_args import JobArgs
from jobs.train_job import TrainJob
from models.base_models.supported_base_model import SupportedBaseModel
from train.gan.gan_trainer import GanTrainer


class GanTrainJob(TrainJob):
    """
    Job to train a GAN-BERT for trace prediction.
    """

    def __init__(self, job_args: JobArgs):
        job_args.base_model = SupportedBaseModel.AUTO_MODEL
        super().__init__(job_args)

    def get_trainer(self, **kwargs) -> GanTrainer:
        """
        Gets the trace trainer for the job
        :return: the trainer
        """
        if self._trainer is None:
            self._trainer = GanTrainer(args=self.trace_args, model_generator=self.get_model_generator(), **kwargs)
        return self._trainer

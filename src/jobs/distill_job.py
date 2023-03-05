from data.managers.trainer_dataset_manager import TrainerDatasetManager
from jobs.components.job_args import JobArgs
from jobs.train_job import TrainJob
from models.model_manager import ModelManager
from train.distill_trainer import DistillTrainer
from train.trace_trainer import TraceTrainer
from train.trainer_args import TrainerArgs
from util.override import overrides


class DistillJob(TrainJob):

    def __init__(self, job_args: JobArgs, student_model_manager: ModelManager, teacher_model_manager: ModelManager,
                 trainer_dataset_manager: TrainerDatasetManager, trainer_args: TrainerArgs):
        """
        The base job class for tracing jobs
        :param job_args: the arguments for the job
        :param student_model_manager: the manages the model necessary for the student
        :param teacher_model_manager: the manages the model necessary for the teacher
        :param trainer_dataset_manager: manages all datasets for the trainer
        :param trainer_args: other arguments needed for the trainer
        """
        super().__init__(job_args, model_manager=student_model_manager, trainer_dataset_manager=trainer_dataset_manager,
                         trainer_args=trainer_args)
        self.student_model_manager = student_model_manager
        self.teacher_model_manager = teacher_model_manager

    @overrides(TrainJob)
    def get_trainer(self, **kwargs) -> TraceTrainer:
        """
        Gets the trace trainer for the job
        :param kwargs: any additional parameters for the trainer
        :return: the trainer
        """
        if self._trainer is None:
            self._trainer = DistillTrainer(trainer_args=self.trainer_args,
                                           trainer_dataset_manager=self.trainer_dataset_manager,
                                           student_model_manager=self.student_model_manager,
                                           teacher_model_manager=self.teacher_model_manager,
                                           **kwargs)
        return self._trainer

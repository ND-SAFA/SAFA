import shutil

from data.managers.trainer_dataset_manager import TrainerDatasetManager
from jobs.abstract_trace_job import AbstractTraceJob
from jobs.components.job_args import JobArgs
from jobs.components.job_result import JobResult
from models.model_manager import ModelManager
from train.trainer_args import TrainerArgs


class PushModelJob(AbstractTraceJob):

    def __init__(self, job_args: JobArgs, model_manager: ModelManager,
                 trainer_dataset_manager: TrainerDatasetManager, trainer_args: TrainerArgs, hub_path: str):
        """
        Responsible for pushing model to hugging face repo
        :param job_args: the arguments for the job
        :param model_manager: the manages the model necessary for the job
        :param trainer_dataset_manager: manages all datasets for the trainer
        :param trainer_args: other arguments needed for the trainer
        :param hub_path: path where the model should be pushed
        """
        super().__init__(job_args=job_args, model_manager=model_manager, trainer_dataset_manager=trainer_dataset_manager,
                         trainer_args=trainer_args)
        self.hub_path = hub_path

    def _run(self) -> JobResult:
        """
        Pushes a model to hugging face
        :return: the model path
        """
        hub_path = self.hub_path
        shutil.rmtree(self.job_args.output_dir)
        trainer = self.get_trainer()
        trainer.push_to_hub(hub_path)
        shutil.rmtree(self.job_args.output_dir)
        return JobResult.from_dict({JobResult.MODEL_PATH: self.job_args.output_dir})

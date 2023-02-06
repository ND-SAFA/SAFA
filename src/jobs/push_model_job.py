from data.managers.trainer_dataset_manager import TrainerDatasetManager
from jobs.abstract_trace_job import AbstractTraceJob
from jobs.components.job_args import JobArgs
from jobs.components.job_result import JobResult
from models.model_manager import ModelManager
from train.trainer_args import TrainerArgs


class PushModelJob(AbstractTraceJob):

    def __init__(self, job_args: JobArgs, model_manager: ModelManager,
                 trainer_dataset_manager: TrainerDatasetManager, trainer_args: TrainerArgs):
        """
        Responsible for pushing model to hugging face repo
        :param job_args: the arguments for the job
        :param model_manager: the manages the model necessary for the job
        :param trainer_dataset_manager: manages all datasets for the trainer
        :param trainer_args: other arguments needed for the trainer
        """
        super().__init__(job_args=job_args, model_manager=model_manager, trainer_dataset_manager=trainer_dataset_manager,
                         trainer_args=trainer_args)

    def _run(self) -> JobResult:
        """
        Pushes a model to hugging face
        :return: the model path
        """
        assert self.trainer_args.hub_model_id is not None, f"Expected hub_model_id to be defined but found none."
        trainer = self.get_trainer()
        trainer.push_to_hub()
        return JobResult.from_dict({JobResult.MODEL_PATH: self.job_args.output_dir})

from tgen.constants.dataset_constants import NO_ORPHAN_CHECK_VALUE
from tgen.data.creators.trace_dataset_creator import TraceDatasetCreator
from tgen.data.managers.trainer_dataset_manager import TrainerDatasetManager
from tgen.data.prompts.abstract_prompt_creator import AbstractPromptCreator
from tgen.data.readers.api_project_reader import ApiProjectReader
from tgen.data.readers.definitions.api_definition import ApiDefinition
from tgen.jobs.components.args.job_args import JobArgs
from tgen.jobs.trainer_jobs.abstract_trainer_job import AbstractTrainerJob
from tgen.jobs.trainer_jobs.hugging_face_job import HuggingFaceJob
from tgen.jobs.trainer_jobs.llm_job import LLMJob
from tgen.models.model_manager import ModelManager
from tgen.train.args.hugging_face_args import HuggingFaceArgs
from tgen.train.args.open_ai_args import OpenAIArgs
from tgen.train.trainers.trainer_task import TrainerTask
from tgen.util.supported_enum import SupportedEnum


class PredictionJobTypes(SupportedEnum):
    OPENAI = "openai"
    BASE = "base"


class JobCreator:
    """
    Creates experiment definitions for endpoints.
    """

    @staticmethod
    def create_prediction_definition(dataset: ApiDefinition, output_dir: str, prediction_job_type: PredictionJobTypes,
                                     model_path: str = None, prompt_creator: AbstractPromptCreator = None) -> AbstractTrainerJob:
        """
        Creates experiment definition for predicting on dataset using defined job type.
        :param dataset: The dataset to predict on.
        :param output_dir: The output directory to store logs and other job information.
        :param prediction_job_type: The type of job to run prediction on (e.g. OPENAI / Model)
        :param model_path: The path to the model used for prediction.
        :return: Definition defining prediction job.
        """
        eval_project_reader = ApiProjectReader(api_definition=dataset)
        eval_dataset_creator = TraceDatasetCreator(project_reader=eval_project_reader, allowed_orphans=NO_ORPHAN_CHECK_VALUE)
        trainer_dataset_manager = TrainerDatasetManager(eval_dataset_creator=eval_dataset_creator)
        job_args = JobArgs(random_seed=42)

        if prediction_job_type == PredictionJobTypes.OPENAI:
            trainer_args = OpenAIArgs(metrics=None)
            job = LLMJob(task=TrainerTask.PREDICT,
                         trainer_dataset_manager=trainer_dataset_manager,
                         trainer_args=trainer_args,
                         job_args=job_args,
                         prompt_creator=prompt_creator)
            return job
        elif prediction_job_type == PredictionJobTypes.BASE:
            assert model_path is not None, "Expected model_path to be defined for prediction job."
            trainer_args = HuggingFaceArgs(output_dir=output_dir, metrics=None)
            model_manager = ModelManager(model_path=model_path)
            job = HuggingFaceJob(task=TrainerTask.PREDICT,
                                 job_args=job_args,
                                 model_manager=model_manager,
                                 trainer_dataset_manager=trainer_dataset_manager,
                                 trainer_args=trainer_args)
            return job
        else:
            raise NotImplementedError(f"Prediction job is not supported for job type:{prediction_job_type.name}")

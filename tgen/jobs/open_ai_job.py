from tgen.data.managers.trainer_dataset_manager import TrainerDatasetManager
from tgen.data.prompts.abstract_prompt_generator import AbstractPromptGenerator
from tgen.data.prompts.classification_prompt_generator import ClassificationPromptGenerator
from tgen.jobs.abstract_trace_job import AbstractTraceJob
from tgen.jobs.components.job_args import JobArgs
from tgen.jobs.components.job_result import JobResult
from tgen.models.model_manager import ModelManager
from tgen.train.open_ai.open_ai_args import OpenAIArgs
from tgen.train.open_ai.open_ai_task import OpenAITask
from tgen.train.open_ai.open_ai_trainer import OpenAITrainer
from tgen.train.trace_output.abstract_trace_output import AbstractTraceOutput


class OpenAIJob(AbstractTraceJob):
    """
    Job to handle open ai tasks
    """

    def __init__(self, data_output_path: str, task: OpenAITask,
                 trainer_dataset_manager: TrainerDatasetManager, base_model: str = "ada",
                 trainer_args: OpenAIArgs = OpenAIArgs(), prompt_generator: AbstractPromptGenerator = ClassificationPromptGenerator(),
                 job_args: JobArgs = JobArgs()):
        """
        Initializes job with necessary args
        :param base_model: The name of the model
        :param data_output_path: The path to where data files will be saved
        :param trainer_args: The arguments for training and prediction calls
        :param trainer_dataset_manager: The dataset manager for training and prediction
        :param prompt_generator: Determines the expected prompt and completion format
        :param job_args: Args for all tgen jobs
        """
        super().__init__(job_args=job_args, model_manager=ModelManager(model_path=base_model),
                         trainer_dataset_manager=trainer_dataset_manager, trainer_args=trainer_args)
        self.task = task
        self.base_model = base_model
        self.data_output_path = data_output_path
        self.trainer_args = trainer_args
        self.prompt_generator = prompt_generator

    def _run(self) -> JobResult:
        """
        Runs the open_ai job
        :return: The result of the job
        """
        if self.task == OpenAITask.FINE_TUNE:
            res = self.get_trainer().perform_training()
        elif self.task == OpenAITask.PREDICT:
            res = self.get_trainer().perform_prediction()
        else:
            raise RuntimeError("Unknown Task %s" % self.task)
        return JobResult.from_trace_output(res) if isinstance(res, AbstractTraceOutput) else JobResult.from_dict(res)

    def get_trainer(self, **kwargs) -> OpenAITrainer:
        """
        Gets the trace trainer for the job
        :param kwargs: any additional parameters for the trainer
        :return: the trainer
        """
        if self._trainer is None:
            self._trainer = OpenAITrainer(trainer_args=self.trainer_args,
                                          trainer_dataset_manager=self.trainer_dataset_manager,
                                          base_model=self.base_model, data_output_path=self.data_output_path,
                                          prompt_generator=self.prompt_generator)
        return self._trainer

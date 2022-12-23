from jobs.abstract_job import AbstractJob
from jobs.components.job_args import JobArgs
from jobs.components.job_result import JobResult
from models.model_manager import ModelManager


class CreateModelJob(AbstractJob):

    def _run(self) -> JobResult:
        """
        Creates a new model
        :return: the model path
        """
        model = self.model_manager.get_model()
        model.save_pretrained(self.output_dir)
        tokenizer = self.model_manager.get_tokenizer()
        tokenizer.save_pretrained(self.output_dir)
        return JobResult.from_dict({JobResult.MODEL_PATH: self.output_dir})

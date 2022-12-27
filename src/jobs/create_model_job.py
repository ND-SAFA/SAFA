from jobs.abstract_job import AbstractJob
from jobs.components.job_result import JobResult


class CreateModelJob(AbstractJob):

    def _run(self) -> JobResult:
        """
        Creates a new model
        :return: the model path
        """
        model = self.model_manager.get_model()
        model.save_pretrained(self.model_manager.model_output_path)
        tokenizer = self.model_manager.get_tokenizer()
        tokenizer.save_pretrained(self.model_manager.model_output_path)
        return JobResult.from_dict({JobResult.MODEL_PATH: self.model_manager.model_output_path})

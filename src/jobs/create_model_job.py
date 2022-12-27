from jobs.abstract_job import AbstractJob
from jobs.components.job_result import JobResult


class CreateModelJob(AbstractJob):

    def _run(self) -> JobResult:
        """
        Creates a new model
        :return: the model path
        """
        save_path = self.model_manager.model_output_path if self.model_manager.model_output_path else self.model_manager.model_path
        model = self.model_manager.get_model()
        model.save_pretrained(self.model_manager.model_output_path)
        tokenizer = self.model_manager.get_tokenizer()
        tokenizer.save_pretrained(self.model_manager.model_output_path)
        return JobResult.from_dict({JobResult.MODEL_PATH: save_path})

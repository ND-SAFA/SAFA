from jobs.abstract_job import AbstractJob
from jobs.components.job_result import JobResult


class CreateModelJob(AbstractJob):

    def _run(self) -> JobResult:
        """
        Creates a new model
        :return: the model path
        """
        model_generator = self.get_model_manager()
        model = model_generator.get_model()
        model.save_pretrained(self.output_dir)
        tokenizer = model_generator.get_tokenizer()
        tokenizer.save_pretrained(self.output_dir)
        return JobResult.from_dict({JobResult.MODEL_PATH: self.output_dir})

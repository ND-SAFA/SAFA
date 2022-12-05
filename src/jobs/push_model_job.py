from jobs.abstract_job import AbstractJob
from jobs.components.job_result import JobResult


class PushModelJob(AbstractJob):

    def _run(self) -> JobResult:
        """
        Creates a new model
        :return: the model path
        """
        model_generator = self.get_model_generator()
        model = model_generator.get_model()
        model.push_to_hub(self.output_dir, use_temp_dir=True)
        return JobResult.from_dict({JobResult.MODEL_PATH: self.output_dir})

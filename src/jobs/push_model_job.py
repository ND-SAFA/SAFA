from jobs.abstract_trace_job import AbstractTraceJob
from jobs.components.job_result import JobResult


class PushModelJob(AbstractTraceJob):

    def _run(self) -> JobResult:
        """
        Creates a new model
        :return: the model path
        """
        trainer = self.get_trainer()
        trainer.push_to_hub(self.output_dir)
        return JobResult.from_dict({JobResult.MODEL_PATH: self.output_dir})

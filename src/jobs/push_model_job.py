import shutil

from jobs.abstract_trace_job import AbstractTraceJob
from jobs.components.job_result import JobResult


class PushModelJob(AbstractTraceJob):

    def _run(self) -> JobResult:
        """
        Creates a new model
        :return: the model path
        """
        hub_path = self.job_args.hub_path
        shutil.rmtree(self.output_dir)
        assert hub_path is not None, "Expected hub_path to be defined."
        trainer = self.get_trainer()
        trainer.push_to_hub(hub_path)
        shutil.rmtree(self.output_dir)
        return JobResult.from_dict({JobResult.MODEL_PATH: self.output_dir})

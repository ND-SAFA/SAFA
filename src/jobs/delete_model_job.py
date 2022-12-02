import os
import shutil
from jobs.abstract_job import AbstractJob
from jobs.components.job_result import JobResult


class DeleteModelJob(AbstractJob):

    def _run(self) -> JobResult:
        """
        Deletes a new model directory
        :return: Empty Dict
        """
        if os.path.exists(self.model_path):
            shutil.rmtree(self.model_path)
        return JobResult()

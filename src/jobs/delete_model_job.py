from jobs.abstract_job import AbstractJob
from jobs.components.job_result import JobResult
from util.file_util import FileUtil


class DeleteModelJob(AbstractJob):

    def _run(self) -> JobResult:
        """
        Deletes a new model directory
        :return: Empty Dict
        """
        FileUtil.delete_dir(self.model_manager.model_path)
        return JobResult()

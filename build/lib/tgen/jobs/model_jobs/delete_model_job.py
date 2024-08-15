from tgen.jobs.abstract_job import AbstractJob
from common_resources.tools.util.file_util import FileUtil


class DeleteModelJob(AbstractJob):

    def _run(self) -> None:
        """
        Deletes a new model directory
        :return: Empty Dict
        """
        FileUtil.delete_dir(self.model_manager.model_path)

import os
import shutil
from typing import Dict

from jobs.abstract_job import AbstractJob


class DeleteModelJob(AbstractJob):

    def _run(self) -> Dict:
        """
        Deletes a new model directory
        :return: Empty Dict
        """
        if os.path.exists(self.output_dir):
            shutil.rmtree(self.output_dir)
        return {}

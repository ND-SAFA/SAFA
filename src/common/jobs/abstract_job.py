import json
import os
import traceback
import uuid
from abc import ABC, abstractmethod
from threading import Thread
from typing import Dict

from common.api.responses import BaseResponse
from common.jobs.abstract_args_builder import AbstractArgsBuilder
from common.jobs.job_status import Status
from common.storage.safa_storage import SafaStorage


class AbstractJob(Thread, ABC):
    OUTPUT_FILENAME = "output.json"

    def __init__(self, arg_builder: AbstractArgsBuilder = None, output_dir: str = '', save_output: bool = True):
        """
        Base job class
        :param arg_builder: job arguments
        :param output_dir: where to save the results (if not provided, defaults to job_id dir inside output_dir provided in args)
        :param save_output: if True, saves the output of the job
        """
        super().__init__()
        self.args = arg_builder.build() if arg_builder else None
        self.status = Status.NOT_STARTED
        self.result = {}
        self.id = uuid.uuid4()
        self.save_output = save_output
        if not output_dir:
            output_dir = os.path.join(self.args.output_dir, str(self.id))
        self.output_dir = SafaStorage.add_mount_directory(output_dir)
        self.output_filepath = os.path.join(self.output_dir, self.OUTPUT_FILENAME)

    @abstractmethod
    def _run(self) -> Dict:
        """
        Runs job specific logic
        :return: output of job as a dictionary
        """
        pass

    def run(self) -> None:
        """
        Runs the job and saves the output
        """
        self.status = Status.IN_PROGRESS
        try:
            output = self._run()
            self.result.update(output)
            self.status = Status.SUCCESS
        except Exception as e:
            print(traceback.format_exc())
            self.result[BaseResponse.EXCEPTION] = str(e)
            self.status = Status.FAILURE

        output = self.get_output_as_json()
        if self.save_output:
            self._save(output)

    def get_output_as_json(self) -> str:
        """
        Returns the job output as json
        :return: the output as json
        """
        output = self.result
        output[BaseResponse.STATUS] = self.status.value
        return json.dumps(output, indent=4)

    def _save(self, output: str) -> bool:
        """
        Saves the output dictionary as json
        :return: True if save was successful else false
        """
        try:
            SafaStorage.save_to_file(output, self.output_filepath)
            return True
        except Exception:
            print(traceback.format_exc())  # to save in logs
            return False

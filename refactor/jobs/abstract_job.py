import os
import traceback
import uuid
from abc import abstractmethod
from typing import Dict

from api.responses.base_response import BaseResponse
from config.constants import SAVE_OUTPUT_DEFAULT
from jobs.job_status import Status
from server.storage.safa_storage import SafaStorage
from tracer.models.model_generator import ModelGenerator
import json


class AbstractJob:
    OUTPUT_FILENAME = "output.json"

    def __init__(self, model_generator: ModelGenerator, output_dir: str, save_output: bool = SAVE_OUTPUT_DEFAULT):
        """
        The base job class
        :param model_generator: the generates the required model for the job
        :param output_dir: where the model will be saved to
        """
        super().__init__()
        self.status = Status.NOT_STARTED
        self.result = {}
        self.id = uuid.uuid4()
        self.model_generator = model_generator
        self.output_dir = output_dir
        self.output_filepath = os.path.join(self.output_dir, self.OUTPUT_FILENAME)
        self.save_output = save_output

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

        json_output = self._get_output_as_json()
        if self.save_output:
            self._save(json_output)

    def _get_output_as_json(self) -> str:
        """
        Returns the job output as json
        :return: the output as json
        """
        output = self.result
        output[BaseResponse.STATUS] = self.status.value
        return json.dumps(output, indent=4)

    @abstractmethod
    def _run(self) -> Dict:
        """
        Runs job specific logic
        :return: output of job as a dictionary
        """
        pass

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

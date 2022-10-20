import os
import traceback
import uuid
from abc import abstractmethod
from typing import Dict

from api.responses.base_response import BaseResponse
from config.constants import SAVE_OUTPUT_DEFAULT, ADD_MOUNT_DIRECTORY_TO_OUTPUT_DEFAULT, ADD_MOUNT_DIRECTORY_TO_MODEL_DEFAULT
from jobs.job_status import Status
from server.storage.safa_storage import SafaStorage
from tracer.models.base_models.supported_base_model import SupportedBaseModel
from tracer.models.model_generator import ModelGenerator
import json


class AbstractJob:
    OUTPUT_FILENAME = "output.json"

    def __init__(self, model_path: str, base_model: SupportedBaseModel, output_dir: str,
                 add_mount_directory_to_output: bool = ADD_MOUNT_DIRECTORY_TO_OUTPUT_DEFAULT,
                 save_job_output: bool = SAVE_OUTPUT_DEFAULT):
        """
        The base job class
        :param base_model: supported base model name
        :param model_path: where the pretrained model will be loaded from
        :param output_dir: where the model will be saved to
        :param add_mount_directory_to_output: if True, adds mount directory to output path
        :param save_job_output: if True, saves the output to the output_dir
        """
        super().__init__()
        self.status = Status.NOT_STARTED
        self.result = {}
        self.id = uuid.uuid4()
        self.model_generator = ModelGenerator(base_model=base_model, model_path=model_path)
        self.output_dir = SafaStorage.add_mount_directory(output_dir) if add_mount_directory_to_output else output_dir
        self.job_output_filepath = self._get_output_filepath(self.output_dir, self.id)
        self.save_output = save_job_output

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

    @staticmethod
    def _get_output_filepath(output_dir: str, job_id: uuid) -> str:
        """
        Gets the path to the file for job output
        :param output_dir: the directory to output to
        :param job_id: the id of the job
        :return: the filepath
        """
        filename = "job_%s_%s" % (str(job_id), AbstractJob.OUTPUT_FILENAME)
        return os.path.join(output_dir, filename)

    def _save(self, output: str) -> bool:
        """
        Saves the output dictionary as json
        :return: True if save was successful else false
        """
        try:
            SafaStorage.save_to_file(output, self.job_output_filepath)
            return True
        except Exception:
            print(traceback.format_exc())  # to save in logs
            return False

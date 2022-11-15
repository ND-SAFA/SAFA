import json
import os
import traceback
import uuid
from abc import abstractmethod
from typing import Dict

import numpy as np

from api.responses.base_response import BaseResponse
from jobs.job_args import JobArgs
from jobs.job_status import Status
from server.storage.safa_storage import SafaStorage
from tracer.models.model_generator import ModelGenerator


class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)


class AbstractJob:
    OUTPUT_FILENAME = "output.json"

    def __init__(self, job_args: JobArgs, **kwargs):
        """
        The base job class
        :param job_args: The arguments to the job.
        """
        super().__init__()
        self.job_args = job_args
        self.status = Status.NOT_STARTED
        self.result = {}
        self.id = uuid.uuid4()
        self.output_dir = SafaStorage.add_mount_directory(
            job_args.output_dir) if job_args.add_mount_directory_to_output else job_args.output_dir
        self.job_output_filepath = self._get_output_filepath(self.output_dir, self.id)
        self.save_job_output = job_args.save_job_output
        self.base_model = job_args.base_model
        self.model_path = job_args.model_path
        self.__model_generator = None

    def get_model_generator(self) -> ModelGenerator:
        """
        Gets the model generator for the job given a base model and model path
        :return: the model generator
        """
        if self.__model_generator is None:
            self.__model_generator = ModelGenerator(base_model=self.base_model, model_path=self.model_path)
        return self.__model_generator

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
            self.result[BaseResponse.TRACEBACK] = traceback.format_exc()
            self.result[BaseResponse.EXCEPTION] = str(e)
            self.status = Status.FAILURE

        json_output = self._get_output_as_json()
        if self.save_job_output:
            self._save(json_output)
        return json_output

    def _get_output_as_json(self) -> str:
        """
        Returns the job output as json
        :return: the output as json
        """
        output = self.result
        output[BaseResponse.STATUS] = self.status.value
        return json.dumps(output, indent=4, cls=NpEncoder)

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

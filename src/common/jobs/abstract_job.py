import json
import os
import traceback
from abc import ABC, abstractmethod
from threading import Thread
from typing import Dict
import uuid

from common.api.prediction_response import PredictionResponse
from common.config.constants import IS_TEST
from common.jobs.abstract_args_builder import AbstractArgsBuilder
from common.jobs.job_status import Status
from common.storage.gcp_cloud_storage import GCPCloudStorage


class AbstractJob(Thread, ABC):
    OUTPUT_FILENAME = "output.json"

    def __init__(self, arg_builder: AbstractArgsBuilder):
        """
        Base job class
        :param arg_builder: job arguments
        """
        super().__init__()
        self.args = arg_builder.build()
        self.status = Status.NOT_STARTED
        self.result = {}
        self.id = uuid.uuid4()
        self.output_dir = os.path.join(self.args.output_dir, str(self.id))
        self.output_filepath = os.path.join(self.output_dir, self.OUTPUT_FILENAME)
        self._save_method = AbstractJob._save_to_filesystem if IS_TEST else AbstractJob._save_to_storage

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
            self.result[PredictionResponse.EXCEPTION] = str(e)
            self.status = Status.FAILURE

        output = self.get_output_as_json()
        self._save(output)

    def get_output_as_json(self) -> str:
        """
        Returns the job output as json
        :return: the output as json
        """
        output = self.result
        output[PredictionResponse.STATUS] = self.status.value
        return json.dumps(output)

    def _save(self, output: str) -> bool:
        """
        Saves the output dictionary as json
        :return: True if save was successful else false
        """
        try:
            self._save_method(output, self.output_filepath)
            return True
        except Exception:
            print(traceback.format_exc())  # to save in logs
            return False

    @staticmethod
    def _save_to_storage(content: str, output_file_path: str):
        """
        Saves output to file at given path in cloud storage solution.
        :param content: The content of the file to create.
        :param output_file_path: The path to save the file to.
        """
        GCPCloudStorage.upload_file(content, output_file_path)

    @staticmethod
    def _save_to_filesystem(content: str, output_file_path: str):
        """
        Soon to be mock function for saving files to storage but using the filesystem instead.
        :param content: The content of the file to create.
        :param output_file_path: The path to save the file to.
        """
        with AbstractJob.safe_open_w(output_file_path) as file:
            file.write(content)

    @staticmethod
    def safe_open_w(path):
        if not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))
        return open(path, 'w')

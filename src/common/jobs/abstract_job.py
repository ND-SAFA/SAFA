import json
import os
import traceback
from abc import ABC, abstractmethod
from threading import Thread
from typing import Dict

import numpy as np

from common.api.prediction_response import PredictionResponse
from common.jobs.abstract_args_builder import AbstractArgsBuilder
from common.jobs.job_status import Status
from common.storage.gcp_cloud_storage import GCPCloudStorage

DEV = False


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
        output = self.serialize_output(self.result)
        output[PredictionResponse.STATUS] = self.status.value
        return json.dumps(output)

    def _get_output_dir(self) -> str:
        """
        Creates an output dir if non exists and returns the path
        :return: the path to the directory
        """
        return self.args.output_dir

    def _get_output_filepath(self) -> str:
        """
        Gets the path to the output file
        :return: the path to the output file
        """
        return self.args.output_dir

    def _save(self, output: str) -> bool:
        """
        Saves the output dictionary as json
        :return: True if save was successful else false
        """
        try:

            output_file_path = self.args.output_dir
            AbstractJob._save_to_storage(output, output_file_path)
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
    def serialize_output(output_dict: Dict) -> Dict:
        """
        Makes dictionary values json serializable and returns serializable dict
        :param output_dict: output dictionary
        :return: a dictionary that is json serializable
        """
        for key, value in output_dict.items():
            if isinstance(value, np.ndarray):
                output_dict[key] = value.tolist()
        return output_dict

    @staticmethod
    def safe_open_w(path):
        os.makedirs(os.path.dirname(path))
        return open(path, 'w')

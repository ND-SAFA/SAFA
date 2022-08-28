import os
from abc import abstractmethod, ABC
from typing import Dict

from common.jobs.abstract_args_builder import AbstractArgsBuilder
from common.jobs.job_result_key import JobResultKey
from common.jobs.job_status import Status
from threading import Thread
import uuid
import json
import numpy as np


class AbstractJob(Thread, ABC):
    OUTPUT_FILENAME = "output.json"

    def __init__(self, arg_builder: AbstractArgsBuilder):
        """
        Base job class
        :param arg_builder: job arguments
        """
        super().__init__()
        self.id = uuid.uuid4()
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
            self.result[JobResultKey.EXCEPTION.value] = str(e)
            self.status = Status.FAILURE

        output = self.get_output_as_json()
        self._save(output)

    def _get_output_dir(self) -> str:
        """
        Creates an output dir if non exists and returns the path
        :return: the path to the directory
        """
        output_dir = os.path.join(self.args.output_dir, str(self.id))
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        return output_dir

    def _get_output_filepath(self) -> str:
        """
        Gets the path to the output file
        :return: the path to the output file
        """
        return os.path.join(self._get_output_dir(), self.OUTPUT_FILENAME)

    def _save(self, output: str) -> bool:
        """
        Saves the output dictionary as json
        :return: True if save was successful else false
        """
        try:
            output_file_path = self._get_output_filepath()
            with open(output_file_path, "w") as outfile:
                outfile.write(output)
            return True
        except Exception:
            return False

    def get_output_as_json(self) -> str:
        """
        Returns the job output as json
        :return: the output as json
        """
        output = self.serialize_output(self.result)
        output[JobResultKey.STATUS.value] = self.status.value
        return json.dumps(output)

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

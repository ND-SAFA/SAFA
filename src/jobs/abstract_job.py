import os
import random
import threading
import traceback
import uuid
from abc import abstractmethod
from copy import deepcopy
from inspect import getfullargspec
from typing import Dict

from jobs.components.job_args import JobArgs
from jobs.components.job_result import JobResult
from models.model_manager import ModelManager
from server.storage.safa_storage import SafaStorage
from util.base_object import BaseObject
from util.file_util import FileUtil
from util.status import Status


class AbstractJob(threading.Thread, BaseObject):
    OUTPUT_FILENAME = "output.json"

    def __init__(self, job_args: JobArgs, model_manager: ModelManager = None):
        """
        The base job class
        :param job_args: The arguments to the job.
        :param model_manager: the model manager
        """
        super().__init__()
        self.job_args = job_args
        self.model_manager = model_manager
        if self.job_args.random_seed:
            self.set_random_seed(self.job_args.random_seed)
        self.result = JobResult()
        self.id = uuid.uuid4()
        self.save_job_output = job_args.save_job_output

    def run(self) -> None:
        """
        Runs the job and saves the output
        """
        self.result.set_job_status(Status.IN_PROGRESS)
        try:
            run_result = self._run()
            self.result = run_result.update(self.result)
            self.result.set_job_status(Status.SUCCESS)
        except Exception as e:
            print(traceback.format_exc())
            self.result[JobResult.TRACEBACK] = traceback.format_exc()
            self.result[JobResult.EXCEPTION] = str(e)
            self.result.set_job_status(Status.FAILURE)
        if self.save_job_output and self.job_args.output_dir:
            self.save(self.job_args.output_dir)

    @staticmethod
    def set_random_seed(random_seed: int) -> None:
        """
        Sets the random seed used for training
        :param random_seed: the random seed to use
        :return: None
        """
        random.seed(random_seed)
        # transformers.enable_full_determinism(random_seed)

    def get_output_filepath(self, output_dir: str = None) -> str:
        """
        Gets the path to the file for job output
        :param output_dir: the directory to the output
        :return: the filepath
        """
        if output_dir is None:
            output_dir = self.job_args.output_dir
        output_path = os.path.join(output_dir, str(self.id))
        FileUtil.make_dir_safe(output_path)
        return os.path.join(output_path, AbstractJob.OUTPUT_FILENAME)

    @abstractmethod
    def _run(self) -> JobResult:
        """
        Runs job specific logic
        :return: output of job as a dictionary
        """

    def save(self, output_dir: str) -> bool:
        """
        Saves the output dictionary as json
        :param output_dir: the directory to save to
        :return: True if save was successful else false
        """
        try:
            json_output = self.result.to_json()
            job_output_filepath = self.get_output_filepath(output_dir)
            SafaStorage.save_to_file(json_output, job_output_filepath)
            return True
        except Exception:
            print(traceback.format_exc())  # to save in logs
            return False

    def __deepcopy__(self, memodict: Dict = {}) -> "AbstractJob":
        """
        Overrides deepcopy because there is a weird issue with coping threads
        :param memodict: param from orig deepcopy
        :return: the copy of the job
        """
        param_names = getfullargspec(self.__init__).args
        params = {name: deepcopy(getattr(self, name, None)) for name in param_names if name != "self"}
        cpyobj = type(self)(**params)  # shallow copy of whole object
        cpyobj.result = deepcopy(self.result)
        return cpyobj

    def __str__(self) -> str:
        """
        Returns the job represented as a string
        :return: a string representation of the job
        """
        return str(self.id)

import os
import random
import threading
import traceback
import uuid
from abc import abstractmethod
from copy import deepcopy
from inspect import getfullargspec
from typing import Dict

import torch
from transformers import set_seed

from jobs.components.job_args import JobArgs
from jobs.components.job_result import JobResult
from models.model_manager import ModelManager
from util.base_object import BaseObject
from util.file_util import FileUtil
from util.logging.logger_manager import logger
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
        self.result = JobResult()
        self.id = uuid.uuid4()
        self.save_job_output = job_args.save_job_output

    def run(self) -> None:
        """
        Runs the job and saves the output
        """
        logger.log_with_title(f"Starting New {self.get_job_name()} Job with Following Experiment Vars",
                    self.result.get_printable_experiment_vars())
        self.result.set_job_status(Status.IN_PROGRESS)
        try:
            self.set_seed()
            run_result = self._run()
            self.result = run_result.update(self.result)
            self.result.set_job_status(Status.SUCCESS)
        except Exception as e:
            logger.exception("Job failed during run")
            self.result[JobResult.TRACEBACK] = traceback.format_exc()
            self.result[JobResult.EXCEPTION] = str(e)
            self.result.set_job_status(Status.FAILURE)
        if self.save_job_output and self.job_args.output_dir:
            self.save(self.job_args.output_dir)
        self.cleanup()

    def cleanup(self) -> None:
        """
        Removes the model from memory of the model manager.
        :return: None
        """
        if self.model_manager:
            self.model_manager.clear_model()
        torch.cuda.empty_cache()

    @staticmethod
    def set_random_seed(random_seed: int) -> None:
        """
        Sets the random seed used for training
        :param random_seed: the random seed to use
        :return: None
        """
        random.seed(random_seed)
        set_seed(random_seed)
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False

    def get_output_filepath(self, output_dir: str = None) -> str:
        """
        Gets the path to the file for job output
        :param output_dir: the directory to the output
        :return: the filepath
        """
        if output_dir is None:
            output_dir = self.job_args.output_dir
        output_path = os.path.join(output_dir, str(self.id))
        FileUtil.create_dir_safely(output_path)
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
            FileUtil.save_to_file(json_output, job_output_filepath)
            return True
        except Exception:
            logger.exception("Unable to save job output")  # to save in logs
            return False

    def set_seed(self) -> None:
        """
        Sets the random seed for this job.
        :return: None
        """
        if self.job_args.random_seed:
            self.set_random_seed(self.job_args.random_seed)

    def get_job_name(self) -> str:
        """
        Gets the name of the job
        :return: The job name
        """
        return self.__class__.__name__.split("Job")[0]

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

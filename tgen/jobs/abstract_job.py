import os
import threading
import traceback
import uuid
from abc import abstractmethod
from copy import deepcopy
from inspect import getfullargspec
from typing import Dict, Type

import torch
import wandb

from tgen.constants import OUTPUT_FILENAME
from tgen.jobs.components.job_args import JobArgs
from tgen.jobs.components.job_result import JobResult
from tgen.models.model_manager import ModelManager
from tgen.util.base_object import BaseObject
from tgen.util.file_util import FileUtil
from tgen.util.logging.logger_manager import logger
from tgen.util.override import overrides
from tgen.util.random_util import RandomUtil
from tgen.util.status import Status


class AbstractJob(threading.Thread, BaseObject):

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
            if self.job_args.random_seed is not None:
                RandomUtil.set_seed(self.job_args.random_seed)
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
            wandb.finish()
        self.cleanup()

    def cleanup(self) -> None:
        """
        Removes the model from memory of the model manager.
        :return: None
        """
        if self.model_manager:
            self.model_manager.clear_model()
        torch.cuda.empty_cache()

    def get_output_filepath(self, output_dir: str = None) -> str:
        """
        Gets the path to the file for job output
        :param output_dir: the directory to the output
        :return: the filepath
        """
        if output_dir is None:
            output_dir = self.job_args.output_dir
        FileUtil.create_dir_safely(output_dir)
        return os.path.join(output_dir, OUTPUT_FILENAME)

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
            FileUtil.write(json_output, job_output_filepath)
            return True
        except Exception:
            logger.exception("Unable to save job output")  # to save in logs
            return False

    def get_job_name(self) -> str:
        """
        Gets the name of the job
        :return: The job name
        """
        return self.__class__.__name__.split("Job")[0]

    @classmethod
    @overrides(BaseObject)
    def _get_enum_class(cls, child_class_name: str) -> Type:
        """
        Returns the correct enum class mapping name to class given the abstract parent class type and name of child class
        :param child_class_name: the name of the child class
        :return: the enum class mapping name to class
        """
        from tgen.jobs.supported_job_type import SupportedJobType
        return SupportedJobType

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

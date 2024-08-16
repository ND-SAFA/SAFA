import gc
import os
import threading
import traceback
import uuid
from abc import abstractmethod
from copy import deepcopy
from inspect import getfullargspec
from typing import Any, Dict, Type

from gen_common.tools.t_logging.logger_manager import logger
from gen_common.tools.util.base_object import BaseObject
from gen_common.tools.util.file_util import FileUtil
from gen_common.tools.util.override import overrides
from gen_common.tools.util.random_util import RandomUtil
from gen_common.tools.util.reflection_util import ParamScope, ReflectionUtil
from gen_common.tools.util.status import Status
from gen_common.traceability.relationship_manager.model_cache import ModelCache

from tgen.common.constants.experiment_constants import OUTPUT_FILENAME
from tgen.core.wb.wb_manager import WBManager
from tgen.jobs.components.args.job_args import JobArgs
from tgen.jobs.components.job_result import JobResult
from tgen.models.model_manager import ModelManager


class AbstractJob(threading.Thread, BaseObject):

    def __init__(self, job_args: JobArgs = None, model_manager: ModelManager = None, require_data: bool = False):
        """
        The base job class
        :param job_args: The arguments to the job.
        :param require_data: If True, asserts a dataset creator or a dataset are provided.
        :param model_manager: the model manager
        """
        super().__init__()
        self.require_data = require_data
        self.job_args = job_args if job_args else JobArgs()
        self.model_manager = model_manager
        self.id = uuid.uuid4()
        self.result = JobResult(job_id=self.id)
        self.save_job_output = self.job_args.save_job_output
        if self.require_data:
            self.job_args.require_data()

    def run(self) -> JobResult:
        """
        Runs the job and saves the output
        """
        logger.log_with_title(f"Starting New {self.get_job_name()} Job with Following Experiment Vars",
                              self.result.get_printable_experiment_vars())
        self.result.status = Status.IN_PROGRESS
        try:
            if self.job_args.random_seed is not None:
                RandomUtil.set_seed(self.job_args.random_seed)
            run_result = self._run()
            self.result.body = run_result
            self.result.status = Status.SUCCESS
        except Exception as e:
            traceback.print_exc()
            logger.exception("Job failed during run")
            self.result.body = traceback.format_exc()
            self.result.status = Status.FAILURE
        if self.save_job_output and self.job_args.output_dir:
            logger.info(f"Saving job output: {self.job_args.output_dir}")
            self.save(self.job_args.output_dir)
            WBManager.finish()
        self.cleanup()
        return self.result

    def cleanup(self) -> None:
        """
        Removes the model from memory of the model manager.
        :return: None
        """
        ModelCache.clear()
        if self.model_manager:
            self.model_manager.clear_model()
        gc.collect()

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
    def _run(self) -> Any:
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
            traceback.print_exc()
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
        ReflectionUtil.copy_attributes(self, cpyobj, ParamScope.PRIVATE)
        return cpyobj

    def __str__(self) -> str:
        """
        Returns the job represented as a string
        :return: a string representation of the job
        """
        return str(self.id)

import os
import random
import threading
import traceback
import uuid
from abc import abstractmethod

from jobs.job_args import JobArgs
from jobs.results.job_status import JobStatus
from jobs.results.job_result import JobResult
from server.storage.safa_storage import SafaStorage
from tracer.models.model_generator import ModelGenerator


class AbstractJob(threading.Thread):
    OUTPUT_FILENAME = "output.json"

    def __init__(self, job_args: JobArgs, **kwargs):
        """
        The base job class
        :param job_args: The arguments to the job.
        """
        super().__init__()
        self.job_args = job_args
        if job_args.random_seed:
            random.seed(job_args.random_seed)
        self.result = JobResult()
        self.id = uuid.uuid4()
        self.output_dir = job_args.output_dir
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
        self.result.set_job_status(JobStatus.IN_PROGRESS)
        try:
            run_result = self._run()
            self.result = run_result.update(self.result)
            self.result.set_job_status(JobStatus.SUCCESS)
        except Exception as e:
            print(traceback.format_exc())
            self.result[JobResult.TRACEBACK] = traceback.format_exc()
            self.result[JobResult.EXCEPTION] = str(e)
            self.result.set_job_status(JobStatus.FAILURE)
        json_output = self.result.to_json()
        if self.save_job_output:
            self._save(json_output)

    @abstractmethod
    def _run(self) -> JobResult:
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
        output_path = os.path.join(output_dir, str(job_id))
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        return os.path.join(output_path, AbstractJob.OUTPUT_FILENAME)

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

import json
from abc import ABC, abstractmethod
from unittest import mock
from unittest.mock import patch

from tgen.common.util.status import Status
from tgen.jobs.abstract_job import AbstractJob
from tgen.jobs.components.job_result import JobResult
from tgen.models.model_manager import ModelManager
from tgen.testres.base_tests.base_trace_test import BaseTraceTest


class BaseJobTest(BaseTraceTest, ABC):

    @patch.object(ModelManager, '_load_model')
    @patch.object(ModelManager, 'get_tokenizer')
    def _test_run_success(self, get_tokenizer_mock: mock.MagicMock, load_model_mock: mock.MagicMock):
        load_model_mock.return_value = self.get_test_model()
        get_tokenizer_mock.return_value = self.get_test_tokenizer()
        job = self.get_job()
        job.run()
        self.assert_output_on_success(job, job.result)

    @patch.object(ModelManager, "get_model")
    @patch.object(ModelManager, "get_tokenizer")
    def _test_run_failure(self, get_tokenizer_mock: mock.MagicMock, get_model_mock: mock.MagicMock):
        get_tokenizer_mock.return_value = self.get_test_tokenizer()
        get_model_mock.return_value = ValueError()
        job = self.get_job()
        job.run()
        self.assert_output_on_failure(self._load_job_output(job))

    @patch.object(ModelManager, "get_tokenizer")
    @patch.object(ModelManager, "get_model")
    def get_job(self, get_model_mock: mock.MagicMock, get_tokenizer_mock: mock.MagicMock):
        get_model_mock.return_value = self.get_test_model()
        get_tokenizer_mock.return_value = self.get_test_tokenizer()
        return self._get_job()

    @staticmethod
    def _load_job_output(job: AbstractJob):
        with open(job.get_output_filepath(output_dir=job.job_args.output_dir)) as out_file:
            return JobResult.from_dict(json.load(out_file))

    def assert_output_on_success(self, job: AbstractJob, job_result: JobResult, **kwargs):
        self.assert_job_succeeded(job_result)
        self._assert_success(job, job_result, **kwargs)

    def assert_job_succeeded(self, job_result):
        if job_result.status == Status.FAILURE:
            failure_msg = job_result.body
            self.fail(failure_msg)
        self.assertEqual(job_result.status, Status.SUCCESS)

    def assert_output_on_failure(self, job_output: JobResult):
        self.assertEqual(job_output.status, Status.FAILURE)

    @abstractmethod
    def _assert_success(self, job: AbstractJob, job_result: JobResult):
        pass

    @abstractmethod
    def _get_job(self) -> AbstractJob:
        pass

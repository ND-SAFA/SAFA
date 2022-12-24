import json
import os
from abc import ABC, abstractmethod
from copy import deepcopy
from unittest import mock
from unittest.mock import patch

from jobs.abstract_job import AbstractJob
from jobs.components.job_args import JobArgs
from jobs.components.job_result import JobResult
from jobs.components.job_status import JobStatus
from models.model_manager import ModelManager
from test.base_trace_test import BaseTraceTest
from test.paths.paths import TEST_OUTPUT_DIR
from train.trainer_args import TrainerArgs


class BaseJobTest(BaseTraceTest, ABC):
    _JOB_PARAMS_BASE = {"output_dir": TEST_OUTPUT_DIR}

    @patch.object(ModelManager, '_ModelManager__load_model')
    @patch.object(ModelManager, 'get_tokenizer')
    def _test_run_success(self, get_tokenizer_mock: mock.MagicMock, load_model_mock: mock.MagicMock):
        load_model_mock.return_value = self.get_test_model()
        get_tokenizer_mock.return_value = self.get_test_tokenizer()
        job = self.get_job()
        job.run()
        self.assert_output_on_success(self._load_job_output(job))

    @patch.object(ModelManager, "get_model")
    @patch.object(ModelManager, "get_tokenizer")
    def _test_run_failure(self, get_tokenizer_mock: mock.MagicMock, get_model_mock: mock.MagicMock):
        get_tokenizer_mock.return_value = self.get_test_tokenizer()
        get_model_mock.return_value = ValueError()
        job = self.get_job()
        job.run()
        self.assert_output_on_failure(self._load_job_output(job))

    @staticmethod
    def get_job_params(as_api=False):
        job_params = deepcopy(BaseJobTest._JOB_PARAMS_BASE)
        # Step - Replaces casing to snake case
        if as_api:
            job_params = BaseJobTest.parse_kwargs(job_params)
        return job_params

    def get_job_args(self, as_api=False) -> JobArgs:
        test_args = BaseJobTest.get_job_params(as_api=as_api)
        return JobArgs(**test_args)

    def get_trainer_args(self, as_api=False):
        test_args = BaseJobTest.get_job_params(as_api=as_api)
        output_dir = os.path.join(test_args["output_dir"], "trace")
        return TrainerArgs(output_dir=output_dir,
                           **BaseJobTest.TRACE_ARGS_PARAMS)

    @staticmethod
    def parse_kwargs(test_args):
        # Step - Converts base model to string
        parsed_kwargs = {}
        for key, value in test_args.items():
            snake_case_key = ''.join(word.title() for word in key.split('_'))
            snake_case_key = snake_case_key[0:1].lower() + snake_case_key[1:]
            parsed_kwargs[snake_case_key] = value
        parsed_kwargs["baseModel"] = parsed_kwargs["baseModel"].name
        return parsed_kwargs

    @patch.object(ModelManager, "get_tokenizer")
    @patch.object(ModelManager, "get_model")
    def get_job(self, get_model_mock: mock.MagicMock, get_tokenizer_mock: mock.MagicMock):
        get_model_mock.return_value = self.get_test_model()
        get_tokenizer_mock.return_value = self.get_test_tokenizer()
        return self._get_job()

    @staticmethod
    def _load_job_output(job: AbstractJob):
        with open(job.job_output_filepath) as out_file:
            return json.load(out_file)

    def assert_output_on_success(self, output_dict: dict):
        self.assertIn(JobResult.STATUS, output_dict)
        if output_dict[JobResult.STATUS] == JobStatus.FAILURE:
            failure_msg = output_dict[JobResult.EXCEPTION] if JobResult.EXCEPTION in output_dict \
                else "Status is FAILURE but should be SUCCESS"
            if JobResult.TRACEBACK in output_dict:
                failure_msg += "\n " + output_dict[JobResult.TRACEBACK]
            self.fail(failure_msg)
        self.assertEquals(output_dict[JobResult.STATUS], JobStatus.SUCCESS)
        self._assert_success(output_dict)

    def assert_output_on_failure(self, output_dict: dict):
        self.assertIn(JobResult.EXCEPTION, output_dict)
        self.assertIn(JobResult.STATUS, output_dict)
        self.assertEquals(output_dict[JobResult.STATUS], JobStatus.FAILURE)

    @abstractmethod
    def _assert_success(self, output_dict: dict):
        pass

    @abstractmethod
    def _get_job(self) -> AbstractJob:
        pass

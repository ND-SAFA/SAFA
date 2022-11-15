import json
import os
from abc import ABC, abstractmethod
from copy import deepcopy
from unittest import mock
from unittest.mock import patch

from jobs.abstract_job import AbstractJob
from jobs.job_status import Status
from jobs.responses.base_response import BaseResponse
from test.base_trace_test import BaseTraceTest
from test.paths.paths import TEST_OUTPUT_DIR
from tracer.datasets.dataset_role import DatasetRole
from tracer.models.model_generator import ModelGenerator
from tracer.train.trace_args import TraceArgs


class BaseJobTest(BaseTraceTest, ABC):
    _JOB_PARAMS_BASE = {**BaseTraceTest.MODEL_GENERATOR_PARAMS,
                        "output_dir": TEST_OUTPUT_DIR}

    @patch.object(ModelGenerator, '_ModelGenerator__load_model')
    @patch.object(ModelGenerator, 'get_tokenizer')
    def _test_run_success(self, get_tokenizer_mock: mock.MagicMock, load_model_mock: mock.MagicMock):
        load_model_mock.return_value = self.get_test_model()
        get_tokenizer_mock.return_value = self.get_test_tokenizer()
        job = self.get_job()
        job.run()
        self.assert_output_on_success(self._load_job_output(job))

    @patch.object(ModelGenerator, "get_model")
    @patch.object(ModelGenerator, "get_tokenizer")
    def _test_run_failure(self, get_tokenizer_mock: mock.MagicMock, get_model_mock: mock.MagicMock):
        get_tokenizer_mock.return_value = self.get_test_tokenizer()
        get_model_mock.return_value = ValueError()
        job = self.get_job()
        job.run()
        self.assert_output_on_failure(self._load_job_output(job))

    @staticmethod
    def get_test_params(as_api=False, include_base_model=True):
        test_args = deepcopy(BaseJobTest._JOB_PARAMS_BASE)
        if not include_base_model:
            test_args.pop("base_model")
        # Step - Replaces casing to snake case
        if as_api:
            test_args = BaseJobTest.parse_kwargs(test_args)
        return test_args

    def get_test_params_for_trace(self, dataset_role=DatasetRole.TRAIN, include_links=True, as_api=False,
                                  include_pre_processing=False,
                                  include_base_model=True,
                                  split_train_dataset=False):
        test_args = BaseJobTest.get_test_params(as_api=as_api, include_base_model=include_base_model)
        trainer_dataset_container = self.create_trainer_dataset_container(
            self.create_dataset_map(dataset_role, include_links),
            include_pre_processing=include_pre_processing,
            split_train_dataset=split_train_dataset)
        output_dir = os.path.join(test_args["output_dir"], "trace")
        test_args["trace_args"] = TraceArgs(output_dir=output_dir, trainer_dataset_container=trainer_dataset_container,
                                            **BaseJobTest.TRACE_ARGS_PARAMS)
        return test_args

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

    @patch.object(ModelGenerator, "get_tokenizer")
    @patch.object(ModelGenerator, "get_model")
    def get_job(self, get_model_mock: mock.MagicMock, get_tokenizer_mock: mock.MagicMock):
        get_model_mock.return_value = self.get_test_model()
        get_tokenizer_mock.return_value = self.get_test_tokenizer()
        return self._get_job()

    @staticmethod
    def _load_job_output(job: AbstractJob):
        with open(job.job_output_filepath) as out_file:
            return json.load(out_file)

    def assert_output_on_success(self, output_dict: dict):
        self.assertIn(BaseResponse.STATUS, output_dict)
        if output_dict[BaseResponse.STATUS] == Status.FAILURE:
            failure_msg = output_dict[BaseResponse.EXCEPTION] if BaseResponse.EXCEPTION in output_dict \
                else "Status is FAILURE but should be SUCCESS"
            if BaseResponse.TRACEBACK in output_dict:
                failure_msg += "\n " + output_dict[BaseResponse.TRACEBACK]
            self.fail(failure_msg)
        self.assertEquals(output_dict[BaseResponse.STATUS], Status.SUCCESS)
        self._assert_success(output_dict)

    def assert_output_on_failure(self, output_dict: dict):
        self.assertIn(BaseResponse.EXCEPTION, output_dict)
        self.assertIn(BaseResponse.STATUS, output_dict)
        self.assertEquals(output_dict[BaseResponse.STATUS], Status.FAILURE)

    @abstractmethod
    def _assert_success(self, output_dict: dict):
        pass

    @abstractmethod
    def _get_job(self) -> AbstractJob:
        pass

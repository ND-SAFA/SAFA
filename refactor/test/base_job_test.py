import json
from abc import ABC, abstractmethod
from copy import deepcopy
from unittest import mock
from unittest.mock import patch

from api.responses.base_response import BaseResponse
from jobs.abstract_job import AbstractJob
from jobs.job_status import Status
from test.base_trace_test import BaseTraceTest
from test.config.paths import TEST_OUTPUT_DIR
from tracer.dataset.creators.supported_dataset_creator import SupportedDatasetCreator
from tracer.dataset.dataset_role import DatasetRole
from tracer.models.model_generator import ModelGenerator


class BaseJobTest(BaseTraceTest, ABC):
    _JOB_PARAMS_BASE = {**BaseTraceTest.MODEL_GENERATOR_PARAMS,
                        "output_dir": TEST_OUTPUT_DIR}
    _DATASET_PARAMS = {"source_layers": BaseTraceTest.SOURCE_LAYERS,
                       "target_layers": BaseTraceTest.TARGET_LAYERS,
                       "true_links": BaseTraceTest.POS_LINKS}
    _TRACE_ARGS_PARAMS = {
        "resample_rate": 3
    }

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
    def get_test_params(as_api=False, include_pre_processing=True, include_base_model=True):
        test_args = deepcopy(BaseJobTest._JOB_PARAMS_BASE)
        if not include_base_model:
            test_args.pop("base_model")
        if include_pre_processing:
            pre_processing_options, pre_processing_params = BaseTraceTest.PRE_PROCESSING_PARAMS
            test_args["dataset_pre_processing_options"] = {
                DatasetRole.PRE_TRAIN: (pre_processing_options, pre_processing_params)
            }
        # Step - Replaces casing to snake case
        if as_api:
            test_args = BaseJobTest.parse_kwargs(test_args)
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

    @staticmethod
    def create_dataset_map(dataset_role: DatasetRole, include_links=True):
        dataset_params = deepcopy(BaseJobTest._DATASET_PARAMS)
        if not include_links:
            dataset_params.pop("true_links")
        return {dataset_role: (SupportedDatasetCreator.CLASSIC_TRACE, dataset_params)}

    def get_test_params_for_trace(self, dataset_role=DatasetRole.TRAIN, include_links=True, as_api=False,
                                  include_pre_processing=False,
                                  include_base_model=True):
        test_args = BaseJobTest.get_test_params(as_api=as_api, include_pre_processing=include_pre_processing,
                                                include_base_model=include_base_model)
        test_args["datasets_map"] = self.create_dataset_map(dataset_role, include_links=include_links)
        test_args["trace_args_params"] = BaseJobTest._TRACE_ARGS_PARAMS
        return test_args

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

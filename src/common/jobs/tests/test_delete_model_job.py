import json
import os

import mock
from mock import patch

from common.api.responses import BaseResponse
from common.jobs.delete_model_job import DeleteModelJob
from common.jobs.job_status import Status
from test.base_test import BaseTest
from test.config.paths import TEST_OUTPUT_DIR


class TestModelJob(BaseTest):
    TEST_PARAMS = BaseTest.get_test_params(include_artifacts=False)

    def test_run_dir_exists(self):
        self.make_test_output_dir()
        test_model_job = self.get_test_model_job()
        test_model_job.run()
        self.assertFalse(os.path.exists(TEST_OUTPUT_DIR))
        self.output_test_success(test_model_job.result)

    def test_run_dir_does_not_exist(self):
        test_model_job = self.get_test_model_job()
        test_model_job.run()
        self.output_test_success(test_model_job.result)

    def output_test_success(self, output_dict: dict):
        self.assertIn(BaseResponse.STATUS, output_dict)
        self.assertEquals(output_dict[BaseResponse.STATUS], Status.SUCCESS)

    @staticmethod
    def make_test_output_dir():
        if not os.path.exists(TEST_OUTPUT_DIR):
            os.mkdir(TEST_OUTPUT_DIR)
        with open(os.path.join(TEST_OUTPUT_DIR, "test.txt"), "w") as test_file:
            test_file.write("This is a test.")
            
    def get_test_model_job(self):
        return DeleteModelJob(output_dir=TEST_OUTPUT_DIR)

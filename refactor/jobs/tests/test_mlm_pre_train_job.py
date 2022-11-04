import os
from unittest.mock import patch

from jobs.mlm_pre_train_job import MLMPreTrainJob
from test.base_test import BaseTest
from test.config.paths import TEST_DATA_DIR, TEST_OUTPUT_DIR
from tracer.models.model_generator import ModelGenerator


class TestMLMPreTrainJob(BaseTest):
    PRETRAIN_DIR = os.path.join(TEST_DATA_DIR, "pre_train")

    @patch.object(ModelGenerator, "get_tokenizer")
    @patch.object(ModelGenerator, "get_model")
    def test_run(self, get_model_mock, get_tokenizer_mock):
        get_model_mock.return_value = self.get_test_model()
        get_tokenizer_mock.return_value = self.get_test_tokenizer()
        job = self.get_job()
        job.run()
        output_file_path = job.job_output_filepath
        with open(output_file_path, "r") as outfile:
            lines = outfile.readlines()
        json_str = "".join(lines)
        print(json_str)

    def get_job(self):
        params = self.get_test_params(include_trace_params=False, include_pre_processing=True)
        params.pop("base_model")
        return MLMPreTrainJob(orig_data_path=self.PRETRAIN_DIR,
                              training_data_dir=TEST_OUTPUT_DIR,
                              **params)

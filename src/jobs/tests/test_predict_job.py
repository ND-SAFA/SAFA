from data.datasets.dataset_role import DatasetRole
from jobs.components.job_args import JobArgs
from jobs.predict_job import PredictJob
from jobs.tests.base_job_test import BaseJobTest


class TestPredictJob(BaseJobTest):
    definition = {
        "job_args": {
            "output_dir": TEST_OUTPUT_DIR
        },
        "model_manager": {
            "model_path": "roberta-base"
        },
        "trainer_dataset_manager": {
            "eval_dataset_creator": {
                "objectType": "Safa",
                "project_path": os.path.join(TEST_DATA_DIR, "safa")
            }
        },
        "trainer_args": {
            "output_dir": TEST_OUTPUT_DIR
        }
    }

    def test_run_success(self):
        self._test_run_success()

    def test_run_failure(self):
        self._test_run_failure()

    def _get_job(self):
        test_params = self.get_test_params_for_trace(dataset_role=DatasetRole.EVAL, include_links=False)
        job_args = JobArgs(**test_params)
        return PredictJob(job_args)

    def _assert_success(self, output_dict: dict):
        self.assert_prediction_output_matches_expected(output_dict)

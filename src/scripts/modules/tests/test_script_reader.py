import os

from jobs.components.job_result import JobResult
from scripts.modules.script_reader import ScriptOutputReader
from testres.base_test import BaseTest
from testres.paths.paths import TEST_RESULT_READER
from testres.test_assertions import TestAssertions


class TestResultReader(BaseTest):
    """
    Tests the correctness of the result reader.
    """
    EXPERIMENT_PATH = os.path.join(TEST_RESULT_READER, "jobs")
    EXPERIMENT_ID = "e9fb497b-390a-4a5e-b1c9-92177d3dc761"
    STEP_ID = "050139d9-3f4e-4c3e-af5a-abefae5e79dd"
    TEST_ENTRY = {
        JobResult.PREDICTION_OUTPUT: {
            JobResult.METRICS: {"a": 1, "b": 2, "c": 3}
        },
        JobResult.VAL_METRICS: {
            0: {"a": 1, "b": 2, "c": 3},
            1: {"a": 3, "b": 6, "c": 9}
        }
    }
    EXPECTED_VAL_METRICS = {"map": 0.242, "ap": 0.0819, "map@1": 1.0, "map@2": 1.0,
                            "map@3": 0.777, "f1": 0.177, "f2": 0.3497,
                            "precision@1": 0.105, "precision@2": 0.053, "precision@3": 0.053}
    EXPECTED_EVAL_METRICS = {"map": 0.194, "ap": 0.0769, "map@1": 1.0, "map@2": 1.0,
                             "map@3": 1.0, "f1": 0.16, "f2": 0.314, "precision@1": 0.053,
                             "precision@2": 0.053, "precision@3": 0.035}

    def test_read(self):
        result_reader = ScriptOutputReader(self.EXPERIMENT_PATH, export=False)
        val_df, eval_df = result_reader.read()
        self.assertEqual(1, len(val_df))
        self.assertEqual(1, len(eval_df))
        TestAssertions.verify_row_contains(self, eval_df.iloc[0], self.EXPECTED_EVAL_METRICS)
        TestAssertions.verify_row_contains(self, val_df.iloc[0], self.EXPECTED_VAL_METRICS)

    def test_read_validation_entries(self) -> None:
        """
        Tests that all validation entries are read and metrics extracted.
        """
        val_entries = ScriptOutputReader.read_validation_entries(self.TEST_ENTRY, ["a", "c"])
        self.assertEqual(2, len(val_entries))
        for i, (a, c) in enumerate([(1, 3), (3, 9)]):
            val_entry = val_entries[i]
            self.assertEqual(a, val_entry["a"])
            self.assertEqual(c, val_entry["c"])

    def test_read_eval_entry(self) -> None:
        """
        Tests that eval metric for job result is able to be read.
        """
        eval_entry = ScriptOutputReader.read_eval_entry(self.TEST_ENTRY, ["a", "b"])
        self.assertEqual(1, eval_entry["a"])
        self.assertEqual(2, eval_entry["b"])

    def test_read_experiment_jobs(self) -> None:
        """
        Tests that output files are all found.
        """
        experiment_results = ScriptOutputReader.read_experiment_jobs(self.EXPERIMENT_PATH)
        self.assertEqual(1, len(experiment_results))
        step_path = experiment_results[0]
        self.assertIn(self.EXPERIMENT_ID, step_path)
        self.assertIn(self.STEP_ID, step_path)

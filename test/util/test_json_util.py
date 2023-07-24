import json
import os

from tgen.common.util.json_util import JsonUtil
from tgen.core.save_strategy.save_strategy_stage import SaveStrategyStage
from tgen.core.trace_output.stage_eval import StageEval
from tgen.core.trace_output.trace_prediction_output import TracePredictionOutput
from tgen.core.trace_output.trace_train_output import TraceTrainOutput
from tgen.testres.base_tests.base_test import BaseTest
from tgen.testres.paths.paths import TEST_DATA_DIR


class TestJsonUtil(BaseTest):
    """
    Responsible for testing JSON utility methods
    """

    def test_read_jsonl_file(self):
        """
        Tests the ability to read a file of .jsonl format
        """
        jsonl_file_path = os.path.join(TEST_DATA_DIR, "prompt", "lhp.jsonl")
        jsonl_dict = JsonUtil.read_jsonl_file(jsonl_file_path)
        with open(jsonl_file_path) as file:
            expected_prompts = file.readlines()
        single_prompt = json.loads(expected_prompts[0])
        for key in single_prompt.keys():
            self.assertIn(key, jsonl_dict)
            self.assertEqual(len(expected_prompts), len(jsonl_dict[key]))

    def test_get_property(self):
        """
        Tests ability to retrieve property in definition when present and catch error otherwise.
        """
        prop_name = "prop_name"
        prop_value = 1
        retrieved_value = JsonUtil.get_property({prop_name: prop_value}, prop_name)
        self.assertEqual(prop_value, retrieved_value)

    def test_get_property_default_value(self):
        """
        Tests ability to retrieve property in definition when present and catch error otherwise.
        """
        prop_name = "prop_name"
        default_value = 1
        retrieved_value = JsonUtil.get_property({}, prop_name, default_value)
        self.assertEqual(default_value, retrieved_value)

    def test_get_property_missing(self):
        """
        Tests ability to retrieve property in definition when present and catch error otherwise.
        """
        prop_name = "missing_prop_name"
        with self.assertRaises(ValueError) as e:
            JsonUtil.get_property({}, prop_name)
        error_message = " ".join(map(str, e.exception.args))
        self.assertIn(prop_name, error_message)

    def test_jsonify(self):
        """
        Tests that objects can be recursively constructed into serializable dictionary.
        TODO: Does this test unsupported functionality?
        """
        t_loss = 10
        metrics = {"map": .34}
        stage_eval = StageEval(stage=SaveStrategyStage.EPOCH,
                               iteration=1,
                               metrics=metrics)
        eval_prediction_output = TracePredictionOutput(metrics=metrics)
        trace_train_output = TraceTrainOutput(global_step=1, training_loss=t_loss, metrics=[],
                                              val_metrics=[stage_eval],
                                              prediction_output=eval_prediction_output)
        output_json = JsonUtil.to_dict(trace_train_output)
        resulting_keys = list(output_json.keys())
        expected_keys = ["global_step", "training_loss", "metrics", "val_metrics", "prediction_output", "training_time"]
        self.assertSetEqual(set(expected_keys), set(resulting_keys))
        self.assertEqual(t_loss, output_json["training_loss"])
        # Verify evaluations
        stage_evals_json = output_json["val_metrics"]
        self.assertEqual(1, len(stage_evals_json))
        # Verify metric
        stage_eval_json = stage_evals_json[0]
        self.assertListEqual(["stage", "iteration", "metrics"], list(stage_eval_json.keys()))
        metric_json = stage_eval_json["metrics"]
        self.assertEqual(metrics["map"], metric_json["map"])

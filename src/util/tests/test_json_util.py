from testres.base_test import BaseTest
from train.save_strategy.save_strategy_stage import SaveStrategyStage
from train.trace_output.stage_eval import StageEval
from train.trace_output.trace_train_output import TraceTrainOutput
from util.json_util import JsonUtil


class TestJsonUtil(BaseTest):
    """
    Responsible for testing JSON utility methods
    """

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
        """
        t_loss = 10
        metrics = {"map": .34}
        stage_eval = StageEval(stage=SaveStrategyStage.EPOCH,
                               iteration=1,
                               metrics=metrics)
        eval_metrics = [stage_eval]
        trace_train_output = TraceTrainOutput(global_step=1, training_loss=t_loss, metrics=[], eval_metrics=eval_metrics)
        output_json = JsonUtil.to_dict(trace_train_output)
        self.assertListEqual(["global_step", "training_loss", "metrics", "eval_metrics"], list(output_json.keys()))
        self.assertEqual(t_loss, output_json["training_loss"])
        # Verify evaluations
        stage_evals_json = output_json["eval_metrics"]
        self.assertEqual(1, len(stage_evals_json))
        # Verify metric
        stage_eval_json = stage_evals_json[0]
        self.assertListEqual(["stage", "iteration", "metrics"], list(stage_eval_json.keys()))
        metric_json = stage_eval_json["metrics"]
        self.assertEqual(metrics["map"], metric_json["map"])

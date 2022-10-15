import numpy as np
from transformers.trainer_utils import PredictionOutput

from api.responses import PredictionResponse

TEST_METRIC_RESULTS = {'test_loss': 0.6929082870483398}
TEST_PREDICTIONS = np.array([[0.50035876, 0.49964124],
                             [0.50035876, 0.49964124],
                             [0.50035876, 0.49964124],
                             [0.50035876, 0.49964124],
                             [0.50035876, 0.49964124],
                             [0.50035876, 0.49964124],
                             [0.50035876, 0.49964124],
                             [0.50035876, 0.49964124],
                             [0.50035876, 0.49964124]])
TEST_LABEL_IDS = np.array([1, 0, 0, 1, 0, 0, 0, 1, 0])
TEST_PREDICTION_OUTPUT = PredictionOutput(predictions=TEST_PREDICTIONS,
                                          label_ids=TEST_LABEL_IDS,
                                          metrics=TEST_METRIC_RESULTS)
TEST_PREDICTION_RESPONSE_OUTPUT = {
    PredictionResponse.PREDICTIONS: [{'source': 's1', 'target': 't1', 'score': 0.5025688409805298},
                                     {'source': 's1', 'target': 't2', 'score': 0.5025688409805298},
                                     {'source': 's1', 'target': 't3', 'score': 0.5025688409805298},
                                     {'source': 's2', 'target': 't1', 'score': 0.5025688409805298},
                                     {'source': 's2', 'target': 't2', 'score': 0.5025688409805298},
                                     {'source': 's2', 'target': 't3', 'score': 0.5025688409805298},
                                     {'source': 's3', 'target': 't1', 'score': 0.5025688409805298},
                                     {'source': 's3', 'target': 't2', 'score': 0.5025688409805298},
                                     {'source': 's3', 'target': 't3', 'score': 0.5025688409805298},
                                     {'source': 's4', 'target': 't4', 'score': 0.5025688409805298},
                                     {'source': 's4', 'target': 't5', 'score': 0.5025688409805298},
                                     {'source': 's4', 'target': 't6', 'score': 0.5025688409805298},
                                     {'source': 's5', 'target': 't4', 'score': 0.5025688409805298},
                                     {'source': 's5', 'target': 't5', 'score': 0.5025688409805298},
                                     {'source': 's5', 'target': 't6', 'score': 0.5025688409805298},
                                     {'source': 's6', 'target': 't4', 'score': 0.5025688409805298},
                                     {'source': 's6', 'target': 't5', 'score': 0.5025688409805298},
                                     {'source': 's6', 'target': 't6', 'score': 0.5025688409805298}],
    PredictionResponse.METRICS: {'test_loss': 0.6948729753494263, 'test_runtime': 0.0749,
                                 'test_samples_per_second': 240.328, 'test_steps_per_second': 40.055}}
KEY_ERROR_MESSAGE = "{} not in {}"
VAL_ERROR_MESSAGE = "{} with value {} does not equal expected value of {} {}"
LEN_ERROR = "Length of {} does not match expected"


def assert_output_matches_expected(output: dict, threshold: int = 0.05):
    if PredictionResponse.PREDICTIONS not in output:
        return False, KEY_ERROR_MESSAGE.format(PredictionResponse.PREDICTIONS, output)
    predictions = TEST_PREDICTION_RESPONSE_OUTPUT[PredictionResponse.PREDICTIONS]
    if len(predictions) != len(output[PredictionResponse.PREDICTIONS]):
        return False, LEN_ERROR.format(PredictionResponse.PREDICTIONS)
    for i, link_dict in enumerate(output[PredictionResponse.PREDICTIONS]):
        for key, val in link_dict.items():
            expected_val = predictions[i][key]
            if not assert_val_equals(val, expected_val, threshold):
                False, VAL_ERROR_MESSAGE.format(key, val, expected_val, "in element %f of %s" % i,
                                                PredictionResponse.PREDICTIONS)
    if PredictionResponse.METRICS not in output:
        return False, KEY_ERROR_MESSAGE.format(PredictionResponse.METRICS, output)
    metrics = TEST_PREDICTION_RESPONSE_OUTPUT[PredictionResponse.METRICS]
    for metric in metrics.keys():
        if metric not in output[PredictionResponse.METRICS]:
            return False, KEY_ERROR_MESSAGE.format(PredictionResponse.METRICS, output[PredictionResponse.METRICS])
    return True, "Output Matches"


def assert_val_equals(val: any, expected_val: any, threshold: int = 0.05) -> bool:
    if isinstance(val, float):
        if abs(val - expected_val) >= threshold:
            return False
    else:
        if val != expected_val:
            return False
    return True

import numpy as np

from transformers.trainer_utils import PredictionOutput

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

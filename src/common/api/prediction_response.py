from scipy.special import softmax

from common.config.constants import METRICS_KEY


class PredictionResponse:
    PREDICTIONS = "predictions"
    EXCEPTION = "exception"
    STATUS = "status"
    ARTIFACT_IDS = "ids"
    METRICS = "metrics"
    IDS = "ids"
    SOURCE = "source"
    TARGET = "target"
    SCORE = "score"

    @staticmethod
    def from_output(output: dict) -> dict:
        response = {
            PredictionResponse.PREDICTIONS: [],
            METRICS_KEY: output[METRICS_KEY]
        }
        artifact_ids = output[PredictionResponse.ARTIFACT_IDS]
        scores = output[PredictionResponse.PREDICTIONS]
        for pred_ids, pred_scores in zip(artifact_ids, scores):
            entry = {
                PredictionResponse.SOURCE: pred_ids[0],
                PredictionResponse.TARGET: pred_ids[1],
                PredictionResponse.SCORE: float(softmax(pred_scores)[1])
            }
            response[PredictionResponse.PREDICTIONS].append(entry)
        return response

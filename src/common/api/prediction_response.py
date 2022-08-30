from typing import List

from scipy.special import softmax


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
    def from_output(output: dict, artifact_id_pairs: List[tuple]) -> dict:
        """
        Creates a prediction response from the output of the prediction
        :param output: output from the prediction
        :param artifact_id_pairs: the list of source, target pair ids corresponding to the entries
        :return: response dictionary
        """
        response = {
            PredictionResponse.PREDICTIONS: [],
            PredictionResponse.METRICS: output[PredictionResponse.METRICS],
        }
        artifact_ids = artifact_id_pairs
        scores = output[PredictionResponse.PREDICTIONS]
        for pred_ids, pred_scores in zip(artifact_ids, scores):
            entry = {
                PredictionResponse.SOURCE: pred_ids[0],
                PredictionResponse.TARGET: pred_ids[1],
                PredictionResponse.SCORE: float(softmax(pred_scores)[1])
            }
            response[PredictionResponse.PREDICTIONS].append(entry)
        return response

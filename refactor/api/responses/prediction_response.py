from copy import deepcopy
from typing import List

from api.responses.base_response import BaseResponse


class PredictionResponse(BaseResponse):
    PREDICTIONS = "predictions"
    ARTIFACT_IDS = "ids"
    METRICS = "metrics"
    IDS = "ids"
    SOURCE = "source"
    TARGET = "target"
    SCORE = "score"

    @staticmethod
    def from_output(output: dict, pred_id_pairs: List[tuple]) -> dict:
        """
        Creates a prediction response from the output of the prediction
        :param output: output from the prediction
        :param pred_id_pairs: the list of source, target pair ids corresponding to the entries
        :return: response dictionary
        """
        response = deepcopy(output)
        scores = output[PredictionResponse.PREDICTIONS]
        predictions = []
        for pred_ids, pred_scores in zip(pred_id_pairs, scores):
            entry = {
                PredictionResponse.SOURCE: pred_ids[0],
                PredictionResponse.TARGET: pred_ids[1],
                PredictionResponse.SCORE: float(pred_scores)
            }
            predictions.append(entry)
        response[PredictionResponse.PREDICTIONS] = predictions
        return response

from typing import Union, Dict
from typing import List

from scipy.special import softmax
from drf_yasg.openapi import Schema, FORMAT_UUID, TYPE_STRING, TYPE_INTEGER


class BaseResponse:
    JOB_ID = "jobID"
    EXCEPTION = "exception"
    STATUS = "status"
    MODEL_PATH = "modelPath"
    _properties = {JOB_ID: Schema(type=TYPE_STRING, format=FORMAT_UUID),
                   STATUS: Schema(type=TYPE_INTEGER),
                   MODEL_PATH: Schema(type=TYPE_STRING),
                   EXCEPTION: Schema(type=TYPE_STRING)}

    @staticmethod
    def get_properties(response_keys: Union[str, list]) -> Dict:
        """
        Gets properties used to generate response documentation
        :param response_keys: either a single response key or a list of response keys to get properties for
        :return a dictionary of the response keys mapped to appropriate schema
        """
        if not isinstance(response_keys, list):
            response_keys = [response_keys]
        properties = {}
        for key in response_keys:
            if key in BaseResponse._properties:
                properties[key] = BaseResponse._properties[key]
        return properties


class PredictionResponse(BaseResponse):
    PREDICTIONS = "predictions"
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

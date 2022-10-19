from typing import Union, Dict
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



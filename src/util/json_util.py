from typing import Dict, List
import json
import numpy as np

class NpEncoder(json.JSONEncoder):
    """
    Handles Numpy conversion to json
    """

    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)


class JSONUtil:

    @staticmethod
    def dict_to_json(dict_: Dict) -> str:
        """
        Converts the dictionary to json
        :param dict_: the dictionary
        :return: the dictionary as json
        """
        return json.dumps(dict_, indent=4, cls=NpEncoder)

    @staticmethod
    def require_properties(json_obj: Dict, required_properties: List[str]):
        for required_property in required_properties:
            if required_property not in json_obj:
                raise Exception("Expected {%s} in :" % required_property, json_obj)

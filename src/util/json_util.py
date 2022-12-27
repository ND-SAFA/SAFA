from typing import Dict, List


class JSONUtil:
    @staticmethod
    def require_properties(json_obj: Dict, required_properties: List[str]):
        for required_property in required_properties:
            if required_property not in json_obj:
                raise Exception("Expected {%s} in :" % required_property, json_obj)

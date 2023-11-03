import re
from typing import Dict, List, Type

from tgen.common.util.json_util import JsonUtil
from tgen.scripts.toolset.core.selector import inquirer_value


class RQProxy:
    def __init__(self, rq_path: str):
        self.rq_path = rq_path
        self.rq_json = JsonUtil.read_json_file(rq_path)

    def inquirer_unknown_variables(self, known_variables: Dict) -> Dict:
        values = self.get_json_values(self.rq_json)
        values = [v for v in values if isinstance(v, str) and "[" in v]  # extract values containing variables

        variables = []
        for value in values:
            variables.extend(self.extract_variables(value))

        variable2value = {}
        for variable in variables:
            message = f"{variable}"
            default_value = known_variables[variable] if variable in known_variables else None
            variable_type = self.get_variable_type(variable)
            user_value = inquirer_value(message, variable_type, default_value)
            variable2value[variable] = user_value
        variable2value.update(known_variables)
        return variable2value

    @classmethod
    def get_variable_type(cls, variable: str, default_type: Type = str):
        supported_types = [int, float, str]
        supported_type_map = {f"_{t.__name__.upper()}]": t for t in supported_types}
        for k, v in supported_type_map.items():
            if variable.endswith(k):
                return v
        return default_type

    @classmethod
    def extract_variables(cls, input_string):
        pattern = r'\[([^\[\]]+)\]'
        matches = re.findall(pattern, input_string)
        return [f'[{match}]' for match in matches]

    @classmethod
    def get_json_values(cls, rq_json: Dict) -> List[str]:
        values = []
        for child_key, child_value in rq_json.items():
            if isinstance(child_value, list):
                for i in child_value:
                    values.extend(cls.get_json_values(i))
            elif isinstance(child_value, dict):
                values.extend(cls.get_json_values(child_value))
            else:
                values.append(child_value)
        return values

import json
from typing import Dict

from tgen.common.util.json_util import NpEncoder


class DataEncoder:
    @staticmethod
    def encode(data: Dict) -> Dict:
        """
        Encodes data into pure JSON.
        :param data: The data to encode into JSON.
        :return: The JSON.
        """
        return json.loads(json.dumps(data, cls=NpEncoder))

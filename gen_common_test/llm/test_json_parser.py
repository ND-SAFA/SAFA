import json

from gen_common.util.json_util import JsonUtil
from gen_common_test.base.mock.decorators.anthropic import mock_anthropic
from gen_common_test.base.mock.test_ai_manager import TestAIManager
from gen_common_test.base.tests.base_test import BaseTest

RESPONSE = """
```json
{
    "definition": "L0 likely refers to Level 0 data processing, which is the lowest level of data processing in remote sensing. It typically involves converting raw sensor data into a more usable format, applying basic calibrations, and performing quality checks. In the context of this project, L0 data processing is likely required for generating products from the Geostationary Lightning Mapper (GLM), Geostationary Composited Moisture Imagery (GRB), and other instruments."
}
```
"""


class TestJsonParser(BaseTest):
    @mock_anthropic
    def test_json_parser(self, ai_manager: TestAIManager):
        result = JsonUtil.remove_json_block_definition(RESPONSE)
        result_dict = json.loads(result)
        self.assertIn("definition", result_dict)
        self.assertIsNotNone(result_dict["definition"])

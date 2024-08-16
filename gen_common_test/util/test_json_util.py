import json
import os

from gen_common.infra.experiment.variables.experimental_variable import ExperimentalVariable
from gen_common.llm.response_managers.xml_response_manager import XMLResponseManager
from gen_common.util import DataclassUtil
from gen_common.util.json_util import JsonUtil
from gen_common_test.base_tests.base_test import BaseTest
from gen_common_test.paths.base_paths import TEST_DATA_DIR


class TestJsonUtil(BaseTest):
    """
    Responsible for testing JSON utility methods
    """

    def test_read_jsonl_file(self):
        """
        Tests the ability to read a file of .jsonl format
        """
        jsonl_file_path = os.path.join(TEST_DATA_DIR, "prompt", "lhp.jsonl")
        jsonl_dict = JsonUtil.read_jsonl_file(jsonl_file_path)
        with open(jsonl_file_path) as file:
            expected_prompts = file.readlines()
        single_prompt = json.loads(expected_prompts[0])
        for key in single_prompt.keys():
            self.assertIn(key, jsonl_dict)
            self.assertEqual(len(expected_prompts), len(jsonl_dict[key]))

    def test_get_property(self):
        """
        Tests ability to retrieve property in definition when present and catch error otherwise.
        """
        prop_name = "prop_name"
        prop_value = 1
        retrieved_value = JsonUtil.get_property({prop_name: prop_value}, prop_name)
        self.assertEqual(prop_value, retrieved_value)

    def test_get_property_default_value(self):
        """
        Tests ability to retrieve property in definition when present and catch error otherwise.
        """
        prop_name = "prop_name"
        default_value = 1
        retrieved_value = JsonUtil.get_property({}, prop_name, default_value)
        self.assertEqual(default_value, retrieved_value)

    def test_get_property_missing(self):
        """
        Tests ability to retrieve property in definition when present and catch error otherwise.
        """
        prop_name = "missing_prop_name"
        with self.assertRaises(ValueError) as e:
            JsonUtil.get_property({}, prop_name)
        error_message = " ".join(map(str, e.exception.args))
        self.assertIn(prop_name, error_message)

    def test_jsonify(self):
        """
        Tests that objects can be recursively constructed into serializable dictionary.
        TODO: Does this test unsupported functionality?
        """
        response_manager = XMLResponseManager(response_tag={"response": ["child1", "child2"]},
                                              expected_responses={"response": ExperimentalVariable(values=[1, 2, 3])})
        output_json = JsonUtil.to_dict(response_manager)
        resulting_keys = list(output_json.keys())
        expected_keys = DataclassUtil.convert_to_dict(response_manager, include_init_vals_only=True).keys()
        self.assertSetEqual(set(expected_keys), set(resulting_keys))
        self.assertDictEqual(output_json["response_tag"], response_manager.response_tag)
        self.assertListEqual(output_json["expected_responses"]["response"], [1, 2, 3])

    def test_get_all_fields(self):
        json_dict = {
            "user": {
                "name": "John Doe",
                "contact": {
                    "email": "john.doe@example.com",
                    "phones": ["+123456789", "+987654321"]
                },
                "address": {
                    "primary": {
                        "street": "123 Main St",
                        "coordinates": {
                            "latitude": 40.7128,
                            "longitude": -74.0060
                        }
                    }
                },
                "orders": [
                    {
                        "date": "2023-05-16T08:30:00Z",
                        "items": [
                            {
                                "productId": "A1B2C3",
                                "quantity": 2,
                                "price": 19.99
                            },
                            {
                                "productId": "D4E5F6",
                                "quantity": 1,
                                "price": 49.99
                            }
                        ],
                        "total": 89.97,
                    },
                    {
                        "orderId": 456,
                        "items": [
                            {
                                "productId": "G7H8I9",
                                "quantity": 3,
                                "price": 9.99
                            }
                        ],
                        "total": 29.97,
                    }
                ]
            }}
        expected_fields = {"user", "name", "contact", "email", "phones", "address", "primary", "street", "coordinates", "latitude",
                           "longitude", "orders", "date", "items", "productId", "quantity", "price", "total", "orderId"}

        fields = JsonUtil.get_all_fields(obj=json_dict)
        self.assertSetEqual(expected_fields, set(fields))

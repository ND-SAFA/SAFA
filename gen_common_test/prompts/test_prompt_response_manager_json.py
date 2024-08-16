import json
from typing import List

from pydantic.v1.main import BaseModel, Field

from gen_common.llm.response_managers.abstract_response_manager import USE_ALL_TAGS
from gen_common.llm.response_managers.json_response_manager import JSONResponseManager
from gen_common.util import DataclassUtil, PromptUtil
from gen_common_test.base_tests.base_test import BaseTest


class FakeResponseModel(BaseModel):
    """
    Response to the user query.
    """
    field1: str = Field(description="This is a field")
    field2: List[str] = Field(
        description="This is a field that is a list and is optional.",
        default_factory=list)


class TestPromptResponseManager(BaseTest):
    EXPECTED_FAIL_VAl = "this failed to parse"

    def test_parse_response(self):
        prm_multi = self.get_multi_tag_prm()
        response_dict1 = {
            "tag1": "one\n",
            "tag2": "2 "
        }
        expected_output1 = {"tag1": ["one"], "tag2": [2], 'tag3': [self.EXPECTED_FAIL_VAl]}
        parsed_response = prm_multi.parse_response(json.dumps(response_dict1))
        self.assertEqual(parsed_response, expected_output1)

        prm_parent_child = self.get_parent_child_tag_prm()
        response_dict2 = {
            "tag1": {
                "tag2": "2!",
                "tag3": ["hello!", "world"]
            }
        }
        expected_output2 = {"parent": [{"c1": [2], "c2": ["hello", "world"]}]}
        parsed_response = prm_parent_child.parse_response(json.dumps(response_dict2))
        self.assertEqual(parsed_response, expected_output2)

        prm_nested = self.get_nested_dict_prm()
        response_dict3 = {
            "tag1": {
                "tag4": [
                    {
                        "tag2": "2!",
                        "tag3": "hello!"
                    },
                    {
                        "tag2": "2!"
                    }
                ],
                "text": 'world'}
        }
        expected_output3 = {'parent': [{"tag4": [{'c1': [2], 'c2': ['hello']},
                                                 {'c1': [2], 'c2': ['this failed to parse']}
                                                 ],
                                        "text": ["world"]}]}
        parsed_response = prm_nested.parse_response(json.dumps(response_dict3))
        self.assertEqual(parsed_response, expected_output3)

        prm_single = self.get_single_tag_prm()
        response_dict4 = {
            "tag1": ["1, 2", "3"]
        }
        expected_output4 = {"tag1": [[1, 2], [3]]}
        parsed_response = prm_single.parse_response(json.dumps(response_dict4))
        self.assertEqual(parsed_response, expected_output4)

        test = prm_single.format_response_instructions()
        test

    def get_single_tag_prm(self) -> JSONResponseManager:
        return JSONResponseManager(response_tag={"tag1": ["v1", "v2"]},
                                   expected_response_type=int,
                                   expected_responses=[1, 2, 3],
                                   value_formatter=lambda tag, val: val.split(",")
                                   )

    def get_parent_child_tag_prm(self) -> JSONResponseManager:
        return JSONResponseManager(response_tag={
            "tag1": {
                "tag2": "value",
                "tag3": "value"
            }
        },
            id2tag={"parent": "tag1", "c1": "tag2", "c2": "tag3"},
            required_tag_ids=USE_ALL_TAGS,
            expected_response_type={"c1": int},
            expected_responses={"c2": ["hello", "world"]},
            default_factory=lambda tag, val: self.EXPECTED_FAIL_VAl,
            value_formatter=lambda tag, val: val.replace("!", ""))

    def get_nested_dict_prm(self) -> JSONResponseManager:
        return JSONResponseManager(response_tag={
            "tag1": {"tag4": [{
                "tag2": "value",
                "tag3": "value"
            }],
                "text": "value"}
        },
            id2tag={"parent": "tag1", "c1": "tag2", "c2": "tag3"},
            required_tag_ids={"c1"},
            expected_response_type={"c1": int},
            expected_responses={"c2": ["hello", "world"]},
            default_factory=lambda tag, val: self.EXPECTED_FAIL_VAl,
            value_formatter=lambda tag, val: val.replace("!", ""))

    def get_multi_tag_prm(self) -> JSONResponseManager:
        return JSONResponseManager(response_tag={
            "tag1": "value",
            "tag2": "value",
            "tag3": "value"
        },
            required_tag_ids="tag1",
            default_factory=lambda tag, val: "this failed to parse",
            expected_response_type={"tag2": int},
            expected_responses=["one", "two", 1, 2],
            value_formatter=lambda tag, val:
            PromptUtil.strip_new_lines_and_extra_space(val))

    def test_to_and_from_langgraph_model(self):
        response_manager1 = JSONResponseManager.from_langgraph_model(FakeResponseModel)
        params = DataclassUtil.convert_to_dict(response_manager1, include_init_vals_only=True)
        response_manager2 = JSONResponseManager(**params)
        response_manager3 = JSONResponseManager.from_langgraph_model(response_manager2.get_langgraph_model())
        for key, var in DataclassUtil.convert_to_dict(response_manager3, include_init_vals_only=True).items():
            self.assertEqual(params[key], var)

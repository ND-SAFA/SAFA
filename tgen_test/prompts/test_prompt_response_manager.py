from typing import Dict

from tgen.common.constants.deliminator_constants import NEW_LINE
from tgen.common.util.prompt_util import PromptUtil
from tgen.prompts.response_managers.abstract_response_manager import USE_ALL_TAGS
from tgen.prompts.response_managers.xml_response_manager import XMLResponseManager
from tgen.testres.base_tests.base_test import BaseTest


class TestPromptResponseManager(BaseTest):
    RESPONSE_FORMAT = "Enclose your first answer in {}, your second in {}, and your third in {}"
    EXPECTED_FAIL_VAl = "this failed to parse"

    def test_parse_response(self):
        prm_multi = self.get_multi_tag_prm()
        parsed_response = prm_multi.parse_response("<tag1>one\n</tag1> and <tag2>2 </tag2>")
        self.assertEqual(parsed_response, {"tag1": ["one"], "tag2": [2], 'tag3': [self.EXPECTED_FAIL_VAl]})

        # missing critical
        try:
            parsed_response_missing = prm_multi.parse_response("<tag>one\n</tag1> and <tag2>2 </tag2>")
            self.fail("Should fail if missing critical tag")
        except Exception:
            pass

        prm_parent_child = self.get_parent_child_tag_prm()
        parsed_response = prm_parent_child.parse_response("<tag1><tag2>2!</tag2><tag3>hello!</tag3><tag3>world</tag3></tag1>")
        self.assertEqual(parsed_response, {"parent": [{"c1": [2], "c2": ["hello", "world"]}]})

        # missing critical
        try:
            parsed_response_missing = prm_parent_child.parse_response("<tag1><tag2>2!</tag2></tag1>")
        except Exception:
            pass

        prm_parent_child = self.get_parent_child_tag_prm()
        prm_parent_child.required_tag_ids.remove("c2")
        parsed_response = prm_parent_child.parse_response("<tag1><tag2>2!</tag2><tag3>hello!</tag3>"
                                                          "</tag1><tag1>world<tag2>2!</tag2></tag1>")
        self.assertEqual(parsed_response, {'parent': [{'c1': [2], 'c2': ['hello']}, {'c1': [2],
                                                                                     'c2': ['this failed to parse'],
                                                                                     'parent': ['world']}]})

        # missing non-critical
        parsed_response_missing = prm_parent_child.parse_response("<tag1><tag2>2!</tag2></tag1>")
        self.assertEqual(parsed_response_missing, {"parent": [{"c1": [2], "c2": [self.EXPECTED_FAIL_VAl]}]})

        prm_single = self.get_single_tag_prm()
        parsed_response = prm_single.parse_response("<tag1>1, 2</tag1>")
        self.assertEqual(parsed_response, {"tag1": [[1, 2]]})

        prm_single = self.get_single_tag_prm()
        parsed_response = prm_single.parse_response("<tag1>1, 2</tag1><tag1>3</tag1>")
        self.assertEqual(parsed_response, {"tag1": [[1, 2], [3]]})

    def test_format_response(self):
        prm_multi = self.get_multi_tag_prm()
        formatted_response = prm_multi._format_response({"tag1": "one\n", "tag2": "2 "})
        self.assertEqual(formatted_response, {"tag1": ["one"], "tag2": [2]})

        prm_multi.loose_response_validation = True
        formatted_response = prm_multi._format_response({"tag1": "onefour", "tag2": "2 "})
        self.assertEqual(formatted_response, {"tag1": ["one"], "tag2": [2]})
        formatted_response = prm_multi._format_response({"tag1": " One", "tag2": "2 "})
        self.assertEqual(formatted_response, {"tag1": ["one"], "tag2": [2]})

        # Not expected response
        formatted_response_bad = prm_multi._format_response({"tag1": "two", "tag2": "4 "})
        self.assertEqual(formatted_response_bad, {"tag1": ["two"], "tag2": [self.EXPECTED_FAIL_VAl]})

        prm_parent_child = self.get_parent_child_tag_prm()
        formatted_response = prm_parent_child._format_response({"parent": {"c1": "2!", "c2": "hello!"}})
        self.assertEqual(formatted_response, {"parent": [{"c1": [2], "c2": ["hello"]}]})

        # Not correct type
        prm_parent_child.required_tag_ids.remove("c1")
        formatted_response_bad = prm_parent_child._format_response({"parent": {"c1": "two!", "c2": "hello!"}})
        self.assertEqual(formatted_response_bad, {"parent": [{"c1": [self.EXPECTED_FAIL_VAl], "c2": ["hello"]}]})

        prm_single = self.get_single_tag_prm()
        formatted_response = prm_single._format_response({"tag1": "1, 2"})
        self.assertEqual(formatted_response, {"tag1": [[1, 2]]})

        # Not an expected response but not default provided
        formatted_response_bad = prm_single._format_response({"tag1": "4, 2"})
        self.assertEqual(formatted_response_bad, {"tag1": [[2]]})

        # Not an expected response type but not default provided
        formatted_response_bad = prm_single._format_response({"tag1": "four, 2"})
        self.assertEqual(formatted_response_bad, {"tag1": [[2]]})

    def test_format_response_instructions(self):
        prm_single = self.get_single_tag_prm()
        self.assertFalse(prm_single.format_response_instructions())  # include response instructions is False

        expected_response = self.RESPONSE_FORMAT.format("<tag1></tag1>", "<tag2></tag2>", "<tag3></tag3>")

        prm_parent_child = self.get_parent_child_tag_prm()
        self.assertEqual(expected_response, prm_parent_child.format_response_instructions())

        prm_multi = self.get_multi_tag_prm()
        self.assertEqual(expected_response, prm_multi.format_response_instructions())

    def test_get_all_tag_ids(self):
        prm_multi = self.get_multi_tag_prm()
        self.assertListEqual(prm_multi.get_all_tag_ids(), ["tag1", "tag2", "tag3"])

        prm_parent_child = self.get_parent_child_tag_prm()
        self.assertListEqual(prm_parent_child.get_all_tag_ids(), ["parent", "c1", "c2"])

        prm_single = self.get_single_tag_prm()
        self.assertListEqual(prm_single.get_all_tag_ids(), ["tag1"])

    def test_custom_formatting(self):
        def format_entry(tag: str, value: Dict):
            return NEW_LINE.join([value["name"][0], value["descr"][0]])

        response_manager = XMLResponseManager(response_tag={"subsystem": ["name", "descr"]},
                                              response_instructions_format="Enclose each sub-system in {} "
                                                                           "with the name of the subsystem inside of "
                                                                           "{} and the description inside of {}.",
                                              entry_formatter=format_entry,
                                              value_formatter=lambda t, v: f"({v})")
        response = "<subsystem><name>S1</name><descr>D1</descr></subsystem>"
        response += "\n<subsystem><name>S2</name><descr>D2</descr></subsystem>"
        parsed_response = response_manager.parse_response(response)
        subsystems = parsed_response["subsystem"]
        self.assertEqual(subsystems[0], "(S1)\n(D1)")
        self.assertEqual(subsystems[1], "(S2)\n(D2)")

    def get_single_tag_prm(self) -> XMLResponseManager:
        return XMLResponseManager(response_tag="tag1",
                                  include_response_instructions=False,
                                  expected_response_type=int,
                                  expected_responses=[1, 2, 3],
                                  value_formatter=lambda tag, val: val.split(",")
                                  )

    def get_parent_child_tag_prm(self) -> XMLResponseManager:
        response_format = self.RESPONSE_FORMAT.format("{parent}", "{c1}", "{c2}")
        return XMLResponseManager(response_tag={"tag1": ["tag2", "tag3"]},
                                  response_instructions_format=response_format,
                                  id2tag={"parent": "tag1", "c1": "tag2", "c2": "tag3"},
                                  required_tag_ids=USE_ALL_TAGS,
                                  expected_response_type={"c1": int},
                                  expected_responses={"c2": ["hello", "world"]},
                                  default_factory=lambda tag, val: self.EXPECTED_FAIL_VAl,
                                  value_formatter=lambda tag, val: val.replace("!", ""))

    def get_multi_tag_prm(self) -> XMLResponseManager:
        return XMLResponseManager(response_tag=["tag1", "tag2", "tag3"],
                                  response_instructions_format=self.RESPONSE_FORMAT,
                                  required_tag_ids="tag1",
                                  default_factory=lambda tag, val: "this failed to parse",
                                  expected_response_type={"tag2": int},
                                  expected_responses=["one", "two", 1, 2],
                                  value_formatter=lambda tag, val:
                                  PromptUtil.strip_new_lines_and_extra_space(val))

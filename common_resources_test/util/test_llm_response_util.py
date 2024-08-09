import uuid

from common_resources.tools.util.llm_response_util import LLMResponseUtil
from common_resources_test.base_tests.base_test import BaseTest


class TestLLMResponseUtil(BaseTest):

    def test_parse(self):
        parsed_response = LLMResponseUtil.parse("<tag1>one\n</tag1> and <tag2>2 </tag2>", "tag1")
        self.assertIn("one\n", parsed_response)
        parsed_response = LLMResponseUtil.parse("<tag1>one\n</tag1> and <tag2>2 </tag2>", "tag2")
        self.assertIn("2 ", parsed_response)
        parsed_response = LLMResponseUtil.parse("<tag1>one\n</tag1> and <tag2>2 </tag2>", "tag3", raise_exception=False)
        self.assertTrue(len(parsed_response) == 0)
        try:
            LLMResponseUtil.parse("<tag1>one\n</tag1> and <tag2>2 </tag2>", "tag3", raise_exception=True)
            self.fail("Should fail if missing critical tag")
        except Exception:
            pass

        parsed_response = LLMResponseUtil.parse("<tag1><tag2>2!</tag2><tag3>hello!</tag3><tag3>world</tag3></tag1>",
                                                "tag1", is_nested=True)[0]
        self.assertIn("tag2", parsed_response)
        self.assertIn("2!", parsed_response["tag2"])
        self.assertIn("tag3", parsed_response)
        self.assertIn("hello!", parsed_response["tag3"])
        self.assertIn("world", parsed_response["tag3"])

        parsed_response = LLMResponseUtil.parse("<tag1><tag2>2!</tag2><tag3>hello!</tag3></tag1><tag1>world<tag2>2!</tag2></tag1>",
                                                "tag1", is_nested=True)
        self.assertIn("tag2", parsed_response[0])
        self.assertIn("tag3", parsed_response[0])
        self.assertIn("tag1", parsed_response[1])
        self.assertIn("tag2", parsed_response[1])

        parsed_response = LLMResponseUtil.parse("<tag1>1, 2</tag1><tag1>3</tag1>", "tag1")
        self.assertIn('1, 2', parsed_response)
        self.assertIn('3', parsed_response)

    def test_extract_predictions_from_response(self):
        id1 = uuid.uuid4()
        id2 = uuid.uuid4()
        response = [{id1: {'tag1': [1], 'tag2': [1, 2]},
                     id2: {'tag3': ["a"], 'tag2ignore': ["some val"]}},
                    {id1: {'tag1': [2], 'tag2': [3, 4]},
                     id2: {'tag3': ["b"], 'tag2ignore': ["some val"]}}
                    ]
        required_ids = {id1, id2}
        required_tags = {"tag1", "tag2", "tag3"}
        result = LLMResponseUtil.extract_predictions_from_response(predictions=response,
                                                                   response_prompt_ids=required_ids,
                                                                   tags_for_response=required_tags)
        self.assert_extracted(response, result, required_ids, required_tags)

        required_ids = id1
        required_tags = {"tag1", "tag2"}
        result = LLMResponseUtil.extract_predictions_from_response(predictions=response,
                                                                   response_prompt_ids=required_ids,
                                                                   tags_for_response=required_tags,
                                                                   return_first=True)
        self.assert_extracted(response, result, required_ids, required_tags, return_first=True)

        required_ids = id1
        required_tags = "tag2"
        result = LLMResponseUtil.extract_predictions_from_response(predictions=response,
                                                                   response_prompt_ids=required_ids,
                                                                   tags_for_response=required_tags)
        self.assert_extracted(response, result, required_ids, required_tags)

        required_ids = id1
        required_tags = "tag1"
        result = LLMResponseUtil.extract_predictions_from_response(predictions=response,
                                                                   response_prompt_ids=required_ids,
                                                                   tags_for_response=required_tags,
                                                                   return_first=True)
        for i, res in enumerate(response):
            self.assertEqual(result[i], res[id1]['tag1'][0])

    def assert_extracted(self, response, result, required_ids, required_tags, return_first: bool = False):
        if not isinstance(required_ids, set):
            required_ids = {required_ids}
        if not isinstance(required_tags, set):
            required_tags = set(required_tags)
        for i, res in enumerate(response):
            extracted = result[i]
            for id_, tags in res.items():
                for tag, val in tags.items():
                    if id_ in required_ids and tag in required_tags:
                        if len(required_tags) > 1:
                            self.assertIn(tag, extracted)
                            extracted_val = extracted[tag]
                        else:
                            extracted_val = val
                        if return_first:
                            self.assertEqual(extracted_val, val[0])
                        else:
                            self.assertEqual(extracted_val, val)
                    else:
                        self.assertNotIn(tag, extracted)

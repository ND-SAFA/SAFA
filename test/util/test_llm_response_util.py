from tgen.testres.base_tests.base_test import BaseTest
from tgen.common.util.llm_response_util import LLMResponseUtil


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

from tgen.testres.base_tests.base_test import BaseTest
from tgen.util.llm_response_util import LLMResponseUtil


class TestLLMResponseUtil(BaseTest):

    def test_parse(self):
        self.assertSize(0, LLMResponseUtil.parse(res="This is a bad response", tag_name="tag", is_nested=True))
        self.assertSize(0, LLMResponseUtil.parse(res="This is a bad response", tag_name="tag", is_nested=False))

        good_response_nested = "<outer><inner>This is a good response</inner></outer>"
        outer = LLMResponseUtil.parse(res=good_response_nested, tag_name="outer", is_nested=True)
        self.assertSize(1, outer)
        self.assertIn("inner", outer[0])

        expected_response = "This is a good response"
        self.assertEqual(expected_response, LLMResponseUtil.parse(res=f"<tag>{expected_response}</tag>", tag_name="tag",
                                                                  is_nested=False)[0])

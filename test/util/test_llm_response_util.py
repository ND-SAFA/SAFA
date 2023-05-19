from bs4.element import Tag

from tgen.testres.base_tests.base_test import BaseTest
from tgen.util.llm_response_util import LLMResponseUtil


class TestLLMResponseUtil(BaseTest):

    def test_parse(self):
        for is_nested in [True, False]:
            self.assertSize(0, LLMResponseUtil.parse(res="This is a bad response", tag_name="tag", is_nested=is_nested))

        good_response_nested = "<outer><inner>This is a good response</inner></outer>"
        outer = LLMResponseUtil.parse(res=good_response_nested, tag_name="outer", is_nested=True)
        self.assertSize(1, outer)
        self.assertIsInstance(outer[0], Tag)

        expected_response = "This is a good response"
        self.assertEqual(expected_response, LLMResponseUtil.parse(res=f"<tag>{expected_response}</tag>", tag_name="tag",
                                                                  is_nested=False))

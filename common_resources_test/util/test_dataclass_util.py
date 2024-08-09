import uuid

from common_resources.llm.prompts.prompt_args import PromptArgs
from common_resources.tools.util.dataclass_util import DataclassUtil
from common_resources_test.base_tests.base_test import BaseTest


class TestDataclasssUtil(BaseTest):

    def test_convert_to_dict(self):
        prompt_id = str(uuid.uuid4())
        prompt_args = PromptArgs(prompt_id=prompt_id, allow_formatting=False)

        dict_ = DataclassUtil.convert_to_dict(prompt_args)
        self.assertEqual(dict_["prompt_id"], prompt_id)
        self.assertEqual(dict_["allow_formatting"], False)

        dict_ = DataclassUtil.convert_to_dict(prompt_args, allow_formatting=True)
        self.assertEqual(dict_["prompt_id"], prompt_id)
        self.assertEqual(dict_["allow_formatting"], True)
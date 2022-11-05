import os
import shutil
from copy import deepcopy

import mock
from django.test import TestCase
from transformers.models.bert.configuration_bert import BertConfig
from transformers.models.bert.tokenization_bert import BertTokenizer
from config.constants import DELETE_TEST_OUTPUT
from server.storage.safa_storage import SafaStorage
from test.config.paths import TEST_OUTPUT_DIR, TEST_VOCAB_FILE
from tracer.models.base_models.pl_bert import PLBert
from tracer.models.base_models.supported_base_model import SupportedBaseModel
from tracer.pre_processing.pre_processing_option import PreProcessingOption


class BaseTest(TestCase):
    MODEL_GENERATOR_PARAMS = {"base_model": SupportedBaseModel.PL_BERT,
                              "model_path": "model"}
    _JOB_PARAMS_BASE = {**MODEL_GENERATOR_PARAMS,
                        "output_dir": TEST_OUTPUT_DIR}
    _TEST_REPLACE_WORD_MAPPINGS = {"This": "Esta", "one": "uno"}
    PRE_PROCESSING_PARAMS = ([PreProcessingOption.REPLACE_WORDS,
                              PreProcessingOption.REMOVE_UNWANTED_CHARS,
                              PreProcessingOption.SEPARATE_JOINED_WORDS,
                              PreProcessingOption.FILTER_MIN_LENGTH],
                             {"word_replace_mappings": _TEST_REPLACE_WORD_MAPPINGS})

    def setup(self):
        if not os.path.isdir(TEST_OUTPUT_DIR):
            SafaStorage.create_dir(TEST_OUTPUT_DIR)

    def tearDown(self):
        if DELETE_TEST_OUTPUT and os.path.exists(TEST_OUTPUT_DIR):
            shutil.rmtree(TEST_OUTPUT_DIR)

    @staticmethod
    def get_test_params(as_api=False, include_pre_processing=False, include_base_model=True):
        test_args = deepcopy(BaseTest._JOB_PARAMS_BASE)
        if not include_base_model:
            test_args.pop("base_model")
        if include_pre_processing:
            pre_processing_options, pre_processing_params = BaseTest.PRE_PROCESSING_PARAMS
            test_args["pre_processing_options"] = pre_processing_options
            test_args["pre_processing_params"] = pre_processing_params
        # Step - Replaces casing to snake case
        if as_api:
            test_args = BaseTest.parse_kwargs(test_args)
        return test_args

    @staticmethod
    def parse_kwargs(test_args):
        # Step - Converts base model to string
        parsed_kwargs = {}
        for key, value in test_args.items():
            snake_case_key = ''.join(word.title() for word in key.split('_'))
            snake_case_key = snake_case_key[0:1].lower() + snake_case_key[1:]
            parsed_kwargs[snake_case_key] = value
        parsed_kwargs["baseModel"] = parsed_kwargs["baseModel"].name
        return parsed_kwargs

    @staticmethod
    def get_test_model():
        return PLBert(BaseTest.get_test_config())

    @staticmethod
    def get_test_config():
        """
        Returns a tiny configuration by default.
        """
        return BertConfig(
            vocab_size=99,
            hidden_size=32,
            num_hidden_layers=5,
            num_attention_heads=4,
            intermediate_size=37,
            hidden_act="gelu",
            hidden_dropout_prob=0.1,
            attention_probs_dropout_prob=0.1,
            max_position_embeddings=512,
            type_vocab_size=16,
            is_decoder=False,
            initializer_range=0.02,
        )

    @staticmethod
    def get_test_tokenizer():
        tokenizer = BertTokenizer(vocab_file=TEST_VOCAB_FILE)
        tokenizer._convert_token_to_id = mock.MagicMock(return_value=24)
        return tokenizer

    def assert_lists_have_the_same_vals(self, list1, list2):
        diff1 = set(list1).difference(list2)
        diff2 = set(list2).difference(list1)
        self.assertEquals(len(diff1), 0)
        self.assertEquals(len(diff2), 0)

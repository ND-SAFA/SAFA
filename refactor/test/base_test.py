import os
import shutil
from copy import deepcopy

import mock
from django.test import TestCase
from transformers.models.bert.configuration_bert import BertConfig
from transformers.models.bert.tokenization_bert import BertTokenizer

from config.constants import DELETE_TEST_OUTPUT, VALIDATION_PERCENTAGE_DEFAULT
from server.storage import SafaStorage
from test.config.paths import TEST_OUTPUT_DIR, TEST_VOCAB_FILE
from test.test_data import TEST_POS_LINKS, TEST_SOURCE_LAYERS, TEST_TARGET_LAYERS
from tracer.models import PLBert, SupportedBaseModel


class BaseTest(TestCase):
    _TEST_ARGS_BASE = {"base_model": SupportedBaseModel.PL_BERT,
                       "model_path": "model",
                       "output_dir": TEST_OUTPUT_DIR,
                       "settings": {"validation_percentage": VALIDATION_PERCENTAGE_DEFAULT}}
    _TEST_ARGS_ARTIFACTS = {"source_layers": TEST_SOURCE_LAYERS,
                            "target_layers": TEST_TARGET_LAYERS,
                            "links": TEST_POS_LINKS,
                            }

    def setup(self):
        if not os.path.isdir(TEST_OUTPUT_DIR):
            SafaStorage.create_dir(TEST_OUTPUT_DIR)

    def tearDown(self):
        if DELETE_TEST_OUTPUT and os.path.exists(TEST_OUTPUT_DIR):
            shutil.rmtree(TEST_OUTPUT_DIR)

    @staticmethod
    def get_test_params(include_artifacts=True, include_links=True, include_settings=True, as_api=False):
        test_args = deepcopy(BaseTest._TEST_ARGS_BASE)
        if not include_settings:
            test_args.pop("settings")
        if include_artifacts:
            test_args.update(BaseTest._TEST_ARGS_ARTIFACTS)
            if not include_links:
                test_args.pop("links")

        # Step - Replaces casing to snake case
        if as_api:
            # Step - Converts base model to string
            parsed_kwargs = {}
            for key, value in test_args.items():
                snake_case_key = ''.join(word.title() for word in key.split('_'))
                snake_case_key = snake_case_key[0:1].lower() + snake_case_key[1:]
                parsed_kwargs[snake_case_key] = value
            parsed_kwargs["baseModel"] = parsed_kwargs["baseModel"].name
            return parsed_kwargs
        else:
            return test_args

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

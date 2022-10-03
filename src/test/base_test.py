import os
import shutil
from copy import deepcopy

from django.test import TestCase

from common.config.constants import DELETE_TEST_OUTPUT
from common.models.base_models.pl_bert import PLBert
from common.models.base_models.supported_base_model import SupportedBaseModel
from common.storage.safa_storage import SafaStorage
from test.config.paths import TEST_OUTPUT_DIR, TEST_VOCAB_FILE
from test.test_data import TEST_POS_LINKS, TEST_SOURCE_LAYERS, TEST_TARGET_LAYERS
from trace.config.constants import VALIDATION_PERCENTAGE_DEFAULT


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
    def get_test_params(include_artifacts=True, include_links=True, include_settings=True):
        test_args = deepcopy(BaseTest._TEST_ARGS_BASE)
        if not include_settings:
            test_args.pop("settings")
        if include_artifacts:
            test_args.update(BaseTest._TEST_ARGS_ARTIFACTS)
            if not include_links:
                test_args.pop("links")
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

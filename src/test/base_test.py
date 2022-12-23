import os
import shutil
from typing import List

import mock
from django.test import TestCase
from transformers import AutoModelForSequenceClassification
from transformers.models.bert.configuration_bert import BertConfig
from transformers.models.bert.tokenization_bert import BertTokenizer

from config.constants import DELETE_TEST_OUTPUT
from data.processing.abstract_data_processing_step import AbstractDataProcessingStep
from data.processing.cleaning.supported_data_cleaning_step import SupportedDataCleaningStep
from test.paths.paths import TEST_DATA_DIR, TEST_OUTPUT_DIR, TEST_VOCAB_FILE


class BaseTest(TestCase):
    MODEL_MANAGER_PARAMS = {
        "model_path": "model"}
    DATA_CLEANING_STEPS: List[AbstractDataProcessingStep] = [
        SupportedDataCleaningStep.REPLACE_WORDS.value(word_replace_mappings={"This": "Esta", "one": "uno"}),
        SupportedDataCleaningStep.REMOVE_UNWANTED_CHARS.value(),
        SupportedDataCleaningStep.SEPARATE_JOINED_WORDS.value(),
        SupportedDataCleaningStep.FILTER_MIN_LENGTH.value()]

    def setUp(self):
        os.makedirs(TEST_OUTPUT_DIR, exist_ok=True)

    def tearDown(self):
        if DELETE_TEST_OUTPUT and os.path.exists(TEST_OUTPUT_DIR):
            shutil.rmtree(TEST_OUTPUT_DIR)
            for file in os.listdir(TEST_DATA_DIR):
                file_path = os.path.join(TEST_DATA_DIR, file)
                if os.path.isfile(file):
                    print(file_path)
                    os.remove(file_path)

    @staticmethod
    def get_test_model():
        return AutoModelForSequenceClassification.from_pretrained("robert-base")

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

    def assert_lists_have_the_same_vals(self, list1, list2):
        diff1 = set(list1).difference(list2)
        diff2 = set(list2).difference(list1)
        self.assertEquals(len(diff1), 0)
        self.assertEquals(len(diff2), 0)

    @staticmethod
    def get_test_tokenizer():
        tokenizer = BertTokenizer(vocab_file=TEST_VOCAB_FILE)
        tokenizer._convert_token_to_id = mock.MagicMock(return_value=24)
        return tokenizer

    @staticmethod
    def read_file(file_path: str):
        with open(file_path) as file:
            return file.read()

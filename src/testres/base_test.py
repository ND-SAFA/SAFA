import os
import shutil
from typing import List, Tuple

import mock
from django.test import TestCase
from transformers import AutoModelForSequenceClassification
from transformers.models.bert.configuration_bert import BertConfig
from transformers.models.bert.tokenization_bert import BertTokenizer

from config.constants import DELETE_TEST_OUTPUT
from data.processing.cleaning.data_cleaner import DataCleaner
from data.processing.cleaning.supported_data_cleaning_step import SupportedDataCleaningStep
from data.tree.artifact import Artifact
from data.tree.trace_link import TraceLink
from testres.paths.paths import TEST_DATA_DIR, TEST_OUTPUT_DIR, TEST_VOCAB_FILE


class BaseTest(TestCase):
    MODEL_MANAGER_PARAMS = {"model_path": "model"}
    DATA_CLEANER = DataCleaner([
        SupportedDataCleaningStep.REPLACE_WORDS.value(word_replace_mappings={"This": "Esta", "one": "uno"}),
        SupportedDataCleaningStep.REMOVE_UNWANTED_CHARS.value(),
        SupportedDataCleaningStep.SEPARATE_JOINED_WORDS.value(),
        SupportedDataCleaningStep.FILTER_MIN_LENGTH.value()])
    BASE_TEST_MODEL = "hf-internal-testing/tiny-random-bert"

    def setUp(self):
        os.makedirs(TEST_OUTPUT_DIR, exist_ok=True)

    def tearDown(self):
        if DELETE_TEST_OUTPUT and os.path.exists(TEST_OUTPUT_DIR):
            shutil.rmtree(TEST_OUTPUT_DIR)
            for file in os.listdir(TEST_DATA_DIR):
                file_path = os.path.join(TEST_DATA_DIR, file)
                if os.path.isfile(file):
                    os.remove(file_path)

    @staticmethod
    def get_test_model():
        return AutoModelForSequenceClassification.from_pretrained(BaseTest.BASE_TEST_MODEL)

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

    @staticmethod
    def read_file(file_path: str):
        with open(file_path) as file:
            return file.read()

    @staticmethod
    def create_trace_links(prefixes: Tuple[str, str], n_artifacts: Tuple[int, int], labels: List[int]):
        """
        Creates trace links between source and targets.
        :param prefixes: The prefix for each artifact type (e.g. source/targets)
        :param n_artifacts: Tuple containing number of artifacts per type
        :param labels: The labels of the trace links.
        :return: Trace links constructed defined by n_sources and n_targets.
        """
        source_prefix, target_prefix = prefixes
        n_source, n_target = n_artifacts
        source_artifacts = BaseTest.create_artifacts(source_prefix, n_source)
        target_artifacts = BaseTest.create_artifacts(target_prefix, n_target)
        trace_links = []
        label_index = 0
        for source_artifact in source_artifacts:
            for target_artifact in target_artifacts:
                is_true_link = labels[label_index] == 1
                trace_links.append(TraceLink(source_artifact, target_artifact, is_true_link))
                label_index += 1
        return trace_links

    @staticmethod
    def create_artifacts(prefix: str, n_artifacts: int, body: str = "body"):
        """
        Creates list of artifacts whose id contain prefix.
        :param prefix: The prefix to name artifact with.
        :param n_artifacts: The number of artifacts to create.
        :param body: The artifact body to supply artifacts with.
        :return: List of artifacts created.
        """
        return [Artifact(prefix + str(i), body) for i in range(n_artifacts)]

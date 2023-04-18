import os
import shutil
from copy import deepcopy
from typing import List, Sized, Tuple
from unittest import TestCase

import mock
from transformers import AutoModelForSequenceClassification
from transformers.models.bert.configuration_bert import BertConfig
from transformers.models.bert.tokenization_bert import BertTokenizer

from tgen.constants import DELETE_TEST_OUTPUT
from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame, ArtifactKeys
from tgen.data.dataframes.trace_dataframe import TraceDataFrame, TraceKeys
from tgen.data.processing.cleaning.data_cleaner import DataCleaner
from tgen.data.processing.cleaning.supported_data_cleaning_step import SupportedDataCleaningStep
from tgen.testres.paths.paths import TEST_OUTPUT_DIR, TEST_VOCAB_FILE
from tgen.util.logging.logger_config import LoggerConfig
from tgen.util.logging.logger_manager import LoggerManager


class BaseTest(TestCase):
    MODEL_MANAGER_PARAMS = {"model_path": "model"}
    DATA_CLEANER = DataCleaner([
        SupportedDataCleaningStep.REPLACE_WORDS.value(word_replace_mappings={"This": "Esta", "one": "uno"}),
        SupportedDataCleaningStep.REMOVE_UNWANTED_CHARS.value(),
        SupportedDataCleaningStep.SEPARATE_JOINED_WORDS.value(),
        SupportedDataCleaningStep.FILTER_MIN_LENGTH.value()])
    BASE_TEST_MODEL = "hf-internal-testing/tiny-random-bert"
    BASE_MODEL_LAYERS = 5  # bert-base = 12
    configure_logging = True

    def assertSize(self, size: int, sized: Sized) -> None:
        """
        Asserts size of list (or other) is equal to given size.
        :param size: The expected size of sized object.
        :param sized: The object whose length is being verified.
        :return: None
        """
        self.assertIsNotNone(sized)
        self.assertEqual(size, len(sized))

    @classmethod
    def setUpClass(cls):
        super(BaseTest, cls).setUpClass()
        if BaseTest.configure_logging:
            config = LoggerConfig(output_dir=TEST_OUTPUT_DIR)
            LoggerManager.configure_logger(config)
            BaseTest.configure_logging = False
            os.makedirs(TEST_OUTPUT_DIR, exist_ok=True)
            wandb_output_path = os.path.join(TEST_OUTPUT_DIR, "wandb")
            os.environ["WANDB_MODE"] = "offline"
            os.environ["WANDB_DIR"] = wandb_output_path

    @classmethod
    def tearDownClass(cls):
        super(BaseTest, cls).tearDownClass()
        BaseTest.remove_output_dir()

    @staticmethod
    def remove_output_dir():
        if DELETE_TEST_OUTPUT and os.path.exists(TEST_OUTPUT_DIR):
            if os.path.isdir(TEST_OUTPUT_DIR):
                shutil.rmtree(TEST_OUTPUT_DIR)
            else:
                os.remove(TEST_OUTPUT_DIR)

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
        trace_links = {TraceKeys.SOURCE.value: [], TraceKeys.TARGET.value: [], TraceKeys.LABEL.value: []}
        label_index = 0
        for s_id, source_artifact in source_artifacts.itertuples():
            for t_id, target_artifact in target_artifacts.itertuples():
                trace_links[TraceKeys.SOURCE.value].append(s_id)
                trace_links[TraceKeys.TARGET.value].append(t_id)
                trace_links[TraceKeys.LABEL.value].append(labels[label_index])
                label_index += 1
        return TraceDataFrame(trace_links)

    @staticmethod
    def create_artifacts(prefix: str, n_artifacts: int, body: str = "body"):
        """
        Creates list of artifacts whose id contain prefix.
        :param prefix: The prefix to name artifact with.
        :param n_artifacts: The number of artifacts to create.
        :param body: The artifact body to supply artifacts with.
        :return: List of artifacts created.
        """
        ids = [prefix + str(i) for i in range(n_artifacts)]
        bodies = [body for i in range(n_artifacts)]
        layer_ids = [1 for i in range(n_artifacts)]
        return ArtifactDataFrame(
            {ArtifactKeys.ID.value: ids, ArtifactKeys.CONTENT.value: bodies, ArtifactKeys.LAYER_ID.value: layer_ids})


SUMMARY_FORMAT = "Summary of {}"


def fake_open_ai_completion(model, prompt, **args):
    choice = {
        "logprobs": {
            "top_logprobs": [
                {
                    " yes": -0.6815379,
                    " no": -1.0818866
                }
            ]
        },
        "text": SUMMARY_FORMAT
    }
    tokens = ["\'".join(p.split('\'')[1:-1]) for p in prompt]
    choices = [deepcopy(choice) for _ in tokens]
    for i, choice in enumerate(choices):
        choice['text'] = choice['text'].format(tokens[i])
    return {"choices": choices, "id": "id"}

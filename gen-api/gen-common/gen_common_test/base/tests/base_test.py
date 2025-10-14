import os
import shutil
from typing import Callable, Dict, List, Sized, Tuple, Type
from unittest import TestCase

import mock
import pandas as pd
from datasets import set_caching_enabled
from transformers import AutoModelForSequenceClassification
from transformers.models.bert.configuration_bert import BertConfig
from transformers.models.bert.tokenization_bert import BertTokenizer

from gen_common.constants import anthropic_constants, environment_constants, open_ai_constants
from gen_common.constants.environment_constants import HF_DATASETS_CACHE
from gen_common.data.dataframes.artifact_dataframe import ArtifactDataFrame
from gen_common.data.dataframes.trace_dataframe import TraceDataFrame
from gen_common.data.keys.structure_keys import ArtifactKeys, TraceKeys
from gen_common.data.processing.cleaning.data_cleaner import DataCleaner
from gen_common.data.processing.cleaning.supported_data_cleaning_step import SupportedDataCleaningStep
from gen_common.infra.t_logging.logger_config import LoggerConfig
from gen_common.infra.t_logging.logger_manager import LoggerManager
from gen_common.util.dataframe_util import DataFrameUtil
from gen_common.util.random_util import RandomUtil
from gen_common_test.base.paths.base_paths import GEN_COMMON_TEST_OUTPUT_PATH, GEN_COMMON_TEST_VOCAB_PATH

DELETE_TEST_OUTPUT = True


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
        environment_constants.IS_TEST = True
        anthropic_constants.ANTHROPIC_MAX_RPM = None
        anthropic_constants.ANTHROPIC_MAX_THREADS = 1
        anthropic_constants.ANTHROPIC_MAX_RE_ATTEMPTS = 1
        open_ai_constants.OPENAI_MAX_THREADS = 1
        open_ai_constants.OPENAI_MAX_ATTEMPTS = 1
        RandomUtil.set_seed(42)
        cache_dir = HF_DATASETS_CACHE
        if cache_dir is None:
            set_caching_enabled(False)
        if BaseTest.configure_logging:
            config = LoggerConfig(output_dir=GEN_COMMON_TEST_OUTPUT_PATH)
            LoggerManager.configure_logger(config)
            BaseTest.configure_logging = False
            os.makedirs(GEN_COMMON_TEST_OUTPUT_PATH, exist_ok=True)
            wandb_output_path = os.path.join(GEN_COMMON_TEST_OUTPUT_PATH, "wandb")
            os.environ["WANDB_MODE"] = "offline"
            os.environ["WANDB_DIR"] = wandb_output_path

    @classmethod
    def tearDownClass(cls):
        super(BaseTest, cls).tearDownClass()
        BaseTest.remove_output_dir()

    @staticmethod
    def remove_output_dir():
        if DELETE_TEST_OUTPUT and os.path.exists(GEN_COMMON_TEST_OUTPUT_PATH):
            if os.path.isdir(GEN_COMMON_TEST_OUTPUT_PATH):
                shutil.rmtree(GEN_COMMON_TEST_OUTPUT_PATH)
            else:
                os.remove(GEN_COMMON_TEST_OUTPUT_PATH)

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
        tokenizer = BertTokenizer(vocab_file=GEN_COMMON_TEST_VOCAB_PATH)
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

    def assert_error(self, callable: Callable, exception_type: Type[Exception], sub_msg: str):
        """
        Expects that callable throws error containing sub-message.
        :param callable: The callable to throw the error.
        :param exception_type: The exception type.
        :param sub_msg: The message to expect to find the exception.
        :return: None
        """
        with self.assertRaises(exception_type) as e:
            callable()
        self.assertIn(sub_msg, e.exception.args[0])

    def assert_lists_have_the_same_vals(self, list1, list2) -> None:
        """
        Tests that list items are identical in both lists.
        :param list1: One of the lists to compare.
        :param list2: The other list to compare.
        :return: None
        """
        diff1 = set(list1).difference(list2)
        diff2 = set(list2).difference(list1)
        self.assertEqual(len(diff1), 0)
        self.assertEqual(len(diff2), 0)

    def verify_entities_in_df(self, expected_entities: List[Dict], entity_df: pd.DataFrame, **kwargs) -> None:
        """
        Verifies that each data frame contains entities given.
        :param entity_df: The data frame expected to contain entities
        :param expected_entities: The entities to verify exist in data frame
        :param kwargs: Any additional parameters to assertion function
        :return: None
        """
        self.assertEqual(len(expected_entities), len(entity_df))
        for entity in expected_entities:
            query_df = DataFrameUtil.query_df(entity_df, entity)
            self.assertEqual(1, len(query_df), msg=f"Could not find row with: {entity}")

import os
import shutil
from copy import deepcopy

import mock
import numpy as np
from django.test import TestCase
from transformers.models.bert.configuration_bert import BertConfig
from transformers.models.bert.tokenization_bert import BertTokenizer
from transformers.trainer_utils import PredictionOutput

from api.responses.prediction_response import PredictionResponse
from config.constants import DELETE_TEST_OUTPUT
from server.storage.safa_storage import SafaStorage
from test.config.paths import TEST_OUTPUT_DIR, TEST_VOCAB_FILE
from tracer.dataset.creators.supported_dataset_creator import SupportedDatasetCreator
from tracer.dataset.data_objects.artifact import Artifact
from tracer.dataset.data_objects.trace_link import TraceLink
from tracer.dataset.dataset_role import DatasetRole
from tracer.models.base_models.pl_bert import PLBert
from tracer.models.base_models.supported_base_model import SupportedBaseModel
from tracer.pre_processing.pre_processing_option import PreProcessingOption


class BaseTest(TestCase):
    SOURCE_LAYERS = [{"s1": "s_token1",
                      "s2": "s_token2",
                      "s3": "s_token3"}, {"s4": "s_token4",
                                          "s5": "s_token5",
                                          "s6": "s_token6"}]

    TARGET_LAYERS = [{"t1": "t_token1",
                      "t2": "t_token2",
                      "t3": "t_token3"}, {"t4": "t_token4",
                                          "t5": "t_token5",
                                          "t6": "t_token6"}]
    ALL_TEST_SOURCES = {id_: token for artifacts in SOURCE_LAYERS for id_, token in artifacts.items()}
    ALL_TEST_TARGETS = {id_: token for artifacts in TARGET_LAYERS for id_, token in artifacts.items()}
    POS_LINKS = [("s1", "t1"), ("s2", "t1"), ("s3", "t2"), ("s4", "t4"), ("s4", "t5"), ("s5", "t6")]
    ALL_TEST_LINKS = [("s1", "t1"), ("s2", "t1"), ("s3", "t1"),
                      ("s1", "t2"), ("s2", "t2"), ("s3", "t2"),
                      ("s1", "t3"), ("s2", "t3"), ("s3", "t3"),
                      ("s4", "t4"), ("s5", "t4"), ("s6", "t4"),
                      ("s4", "t5"), ("s5", "t5"), ("s6", "t5"),
                      ("s4", "t6"), ("s5", "t6"), ("s6", "t6")]
    LINKED_TARGETS = ["t1", "t2", "t4", "t5", "t6"]
    NEG_LINKS = set(ALL_TEST_LINKS).difference(set(POS_LINKS))

    TEST_METRIC_RESULTS = {'test_loss': 0.6929082870483398}
    TEST_PREDICTIONS = np.array([[0.50035876, 0.49964124],
                                 [0.50035876, 0.49964124],
                                 [0.50035876, 0.49964124],
                                 [0.50035876, 0.49964124],
                                 [0.50035876, 0.49964124],
                                 [0.50035876, 0.49964124],
                                 [0.50035876, 0.49964124],
                                 [0.50035876, 0.49964124],
                                 [0.50035876, 0.49964124]])
    TEST_LABEL_IDS = np.array([1, 0, 0, 1, 0, 0, 0, 1, 0])
    TEST_PREDICTION_OUTPUT = PredictionOutput(predictions=TEST_PREDICTIONS,
                                              label_ids=TEST_LABEL_IDS,
                                              metrics=TEST_METRIC_RESULTS)
    TEST_PREDICTION_RESPONSE_OUTPUT = {
        PredictionResponse.PREDICTIONS: [{'source': 's1', 'target': 't3', 'score': 0.4997793138027191},
                                         {'source': 's1', 'target': 't1', 'score': 0.4997793138027191},
                                         {'source': 's4', 'target': 't5', 'score': 0.4997793138027191},
                                         {'source': 's5', 'target': 't6', 'score': 0.4997793138027191},
                                         {'source': 's2', 'target': 't2', 'score': 0.4997793138027191},
                                         {'source': 's5', 'target': 't4', 'score': 0.4997793138027191},
                                         {'source': 's1', 'target': 't2', 'score': 0.4997793138027191},
                                         {'source': 's3', 'target': 't2', 'score': 0.4997793138027191},
                                         {'source': 's4', 'target': 't4', 'score': 0.4997793138027191},
                                         {'source': 's6', 'target': 't5', 'score': 0.4997793138027191},
                                         {'source': 's2', 'target': 't3', 'score': 0.4997793138027191},
                                         {'source': 's5', 'target': 't5', 'score': 0.4997793138027191},
                                         {'source': 's3', 'target': 't1', 'score': 0.4997793138027191},
                                         {'source': 's6', 'target': 't6', 'score': 0.4997793138027191},
                                         {'source': 's4', 'target': 't6', 'score': 0.4997793138027191},
                                         {'source': 's6', 'target': 't4', 'score': 0.4997793138027191},
                                         {'source': 's2', 'target': 't1', 'score': 0.4997793138027191},
                                         {'source': 's3', 'target': 't3', 'score': 0.4997793138027191}],
        PredictionResponse.METRICS: {'test_loss': 0.6948729753494263, 'test_runtime': 0.0749,
                                     'test_samples_per_second': 240.328, 'test_steps_per_second': 40.055}}
    _KEY_ERROR_MESSAGE = "{} not in {}"
    _VAL_ERROR_MESSAGE = "{} with value {} does not equal expected value of {} {}"
    _LEN_ERROR = "Length of {} does not match expected"
    MODEL_GENERATOR_PARAMS = {"base_model": SupportedBaseModel.PL_BERT,
                              "model_path": "model"}
    _JOB_PARAMS_BASE = {**MODEL_GENERATOR_PARAMS,
                        "output_dir": TEST_OUTPUT_DIR}
    _DATASET_PARAMS = {"source_layers": SOURCE_LAYERS,
                       "target_layers": TARGET_LAYERS,
                       "true_links": POS_LINKS}
    _TEST_REPLACE_WORD_MAPPINGS = {"This": "Esta", "one": "uno"}
    PRE_PROCESSING_PARAMS = ([PreProcessingOption.REPLACE_WORDS,
                              PreProcessingOption.REMOVE_UNWANTED_CHARS,
                              PreProcessingOption.SEPARATE_JOINED_WORDS,
                              PreProcessingOption.FILTER_MIN_LENGTH],
                             {"word_replace_mappings": _TEST_REPLACE_WORD_MAPPINGS})

    @staticmethod
    def create_dataset_map(dataset_role: DatasetRole, include_links=True):
        dataset_params = deepcopy(BaseTest._DATASET_PARAMS)
        if not include_links:
            dataset_params.pop("true_links")
        return {dataset_role: (SupportedDatasetCreator.CLASSIC_TRACE, dataset_params)
                }

    def setup(self):
        
        if not os.path.isdir(TEST_OUTPUT_DIR):
            SafaStorage.create_dir(TEST_OUTPUT_DIR)

    def tearDown(self):
        if DELETE_TEST_OUTPUT and os.path.exists(TEST_OUTPUT_DIR):
            shutil.rmtree(TEST_OUTPUT_DIR)

    @staticmethod
    def get_test_params(dataset_role=DatasetRole.TRAIN, include_trace_params=True, include_links=True, as_api=False,
                        include_pre_processing=False):
        test_args = deepcopy(BaseTest._JOB_PARAMS_BASE)
        if include_trace_params:
            test_args["datasets_map"] = BaseTest.create_dataset_map(dataset_role, include_links=include_links)
        if include_pre_processing:
            pre_processing_options, pre_processing_params = BaseTest.PRE_PROCESSING_PARAMS
            test_args["pre_processing_options"] = pre_processing_options
            test_args["pre_processing_params"] = pre_processing_params

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

    def get_links(self, link_list):
        links = {}
        for source, target in link_list:
            link = self.get_test_link(source, target)
            links[link.id] = link
        return links

    def get_link_ids(self, links_list):
        return list(self.get_links(links_list).keys())

    def get_test_link(self, source, target):
        s = Artifact(source, self.ALL_TEST_SOURCES[source])
        t = Artifact(target, self.ALL_TEST_TARGETS[target])
        return TraceLink(s, t)

    def get_test_artifacts(self, artifacts_dict):
        return [Artifact(id_, token) for id_, token in artifacts_dict.items()]

    def assert_output_matches_expected(self, output: dict, threshold: int = 0.05):
        if PredictionResponse.PREDICTIONS not in output:
            self.fail(self._KEY_ERROR_MESSAGE.format(PredictionResponse.PREDICTIONS, output))
        predictions = self.TEST_PREDICTION_RESPONSE_OUTPUT[PredictionResponse.PREDICTIONS]
        if len(predictions) != len(output[PredictionResponse.PREDICTIONS]):
            self.fail(self._LEN_ERROR.format(PredictionResponse.PREDICTIONS))
        # for i, link_dict in enumerate(output[PredictionResponse.PREDICTIONS]):
        #     for key, val in link_dict.items():
        #         expected_val = predictions[i][key]
        #         if not self.assert_val_equals(val, expected_val, threshold):
        #             self.fail(self._VAL_ERROR_MESSAGE.format(key, val, expected_val, "in element %d of %s" % (i,
        #                                                                                                       PredictionResponse.PREDICTIONS)))
        if PredictionResponse.METRICS not in output:
            self.fail(self._KEY_ERROR_MESSAGE.format(PredictionResponse.METRICS, output))
        metrics = self.TEST_PREDICTION_RESPONSE_OUTPUT[PredictionResponse.METRICS]
        for metric in metrics.keys():
            if metric not in output[PredictionResponse.METRICS]:
                self.fail(
                    self._KEY_ERROR_MESSAGE.format(PredictionResponse.METRICS, output[PredictionResponse.METRICS]))

    def assert_val_equals(self, val: any, expected_val: any, threshold: int = 0.05) -> bool:
        if isinstance(val, float):
            if abs(val - expected_val) >= threshold:
                return False
        else:
            if val != expected_val:
                return False
        return True

    def assert_lists_have_the_same_vals(self, list1, list2):
        diff1 = set(list1).difference(list2)
        diff2 = set(list2).difference(list1)
        self.assertEquals(len(diff1), 0)
        self.assertEquals(len(diff2), 0)

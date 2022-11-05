from copy import deepcopy

from api.responses.prediction_response import PredictionResponse
from test.base_test import BaseTest
from tracer.dataset.creators.supported_dataset_creator import SupportedDatasetCreator
from tracer.dataset.data_objects.artifact import Artifact
from tracer.dataset.data_objects.trace_link import TraceLink
from tracer.dataset.dataset_role import DatasetRole
from transformers.trainer_utils import PredictionOutput
import numpy as np


class BaseTraceTest(BaseTest):
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

    _EXAMPLE_METRIC_RESULTS = {'test_loss': 0.6929082870483398}
    _EXAMPLE_PREDICTIONS = np.array([[0.50035876, 0.49964124],
                                     [0.50035876, 0.49964124],
                                     [0.50035876, 0.49964124],
                                     [0.50035876, 0.49964124],
                                     [0.50035876, 0.49964124],
                                     [0.50035876, 0.49964124],
                                     [0.50035876, 0.49964124],
                                     [0.50035876, 0.49964124],
                                     [0.50035876, 0.49964124]])
    _EXAMPLE_LABEL_IDS = np.array([1, 0, 0, 1, 0, 0, 0, 1, 0])
    TEST_PREDICTION_OUTPUT = PredictionOutput(predictions=_EXAMPLE_PREDICTIONS,
                                              label_ids=_EXAMPLE_LABEL_IDS,
                                              metrics=_EXAMPLE_METRIC_RESULTS)
    _EXAMPLE_PREDICTION_LINKS = {'source': 0, 'target': 1, 'score': 0.5}
    _EXAMPLE_PREDICTION_METRICS = {'test_loss': 0.6948729753494263, 'test_runtime': 0.0749,
                                   'test_samples_per_second': 240.328, 'test_steps_per_second': 40.055}
    _DATASET_PARAMS = {"source_layers": SOURCE_LAYERS,
                       "target_layers": TARGET_LAYERS,
                       "true_links": POS_LINKS}
    _KEY_ERROR_MESSAGE = "{} not in {}"
    _VAL_ERROR_MESSAGE = "{} with value {} does not equal expected value of {} {}"
    _LEN_ERROR = "Length of {} does not match expected"

    @staticmethod
    def get_test_params_with_dataset(dataset_role=DatasetRole.TRAIN, include_links=True, as_api=False, include_pre_processing=False,
                                     include_base_model=True):
        test_args = BaseTraceTest.get_test_params(as_api=as_api, include_pre_processing=include_pre_processing,
                                                  include_base_model=include_base_model)
        test_args["datasets_map"] = BaseTraceTest.create_dataset_map(dataset_role, include_links=include_links)
        return test_args

    @staticmethod
    def create_dataset_map(dataset_role: DatasetRole, include_links=True):
        dataset_params = deepcopy(BaseTraceTest._DATASET_PARAMS)
        if not include_links:
            dataset_params.pop("true_links")
        return {dataset_role: (SupportedDatasetCreator.CLASSIC_TRACE, dataset_params)}

    def assert_prediction_output_matches_expected(self, output: dict, threshold: int = 0.05):
        if PredictionResponse.PREDICTIONS not in output:
            self.fail(self._KEY_ERROR_MESSAGE.format(PredictionResponse.PREDICTIONS, output))
        predictions = output[PredictionResponse.PREDICTIONS]
        if len(predictions) != len(self.ALL_TEST_LINKS):
            self.fail(self._LEN_ERROR.format(PredictionResponse.PREDICTIONS))
        expected_links = {link for link in self.ALL_TEST_LINKS}
        predicted_links = set()
        for link_dict in output[PredictionResponse.PREDICTIONS]:
            link = [None, None]
            for key, val in self._EXAMPLE_PREDICTION_LINKS.items():
                if key not in link_dict:
                    self.fail(self._KEY_ERROR_MESSAGE.format(key, PredictionResponse.PREDICTIONS))
                if key == "score":
                    expected_val = self._EXAMPLE_PREDICTION_LINKS["score"]
                    if abs(val - expected_val) >= threshold:
                        self.fail(self._VAL_ERROR_MESSAGE.format(key, val, expected_val, PredictionResponse.PREDICTIONS))
                else:
                    link[val] = link_dict[key]
            predicted_links.add(tuple(link))
        self.assert_lists_have_the_same_vals(expected_links, predicted_links)
        if PredictionResponse.METRICS not in output:
            self.fail(self._KEY_ERROR_MESSAGE.format(PredictionResponse.METRICS, output))
        for metric in self._EXAMPLE_PREDICTION_METRICS.keys():
            if metric not in output[PredictionResponse.METRICS]:
                self.fail(
                    self._KEY_ERROR_MESSAGE.format(PredictionResponse.METRICS, output[PredictionResponse.METRICS]))

    def get_link_ids(self, links_list):
        return list(self.get_links(links_list).keys())

    @staticmethod
    def get_links(link_list):
        links = {}
        for source, target in link_list:
            link = BaseTraceTest.get_test_link(source, target)
            links[link.id] = link
        return links

    @staticmethod
    def get_test_link(source, target):
        s = Artifact(source, BaseTraceTest.ALL_TEST_SOURCES[source])
        t = Artifact(target, BaseTraceTest.ALL_TEST_TARGETS[target])
        return TraceLink(s, t)

    @staticmethod
    def get_test_artifacts(artifacts_dict):
        return [Artifact(id_, token) for id_, token in artifacts_dict.items()]

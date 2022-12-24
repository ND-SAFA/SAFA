from copy import deepcopy
from typing import Dict, List

import numpy as np
from transformers.trainer_utils import PredictionOutput

from config.constants import VALIDATION_PERCENTAGE_DEFAULT
from data.datasets.creators.abstract_dataset_creator import AbstractDatasetCreator
from data.datasets.creators.split_dataset_creator import SplitDatasetCreator
from data.datasets.creators.supported_dataset_creator import SupportedDatasetCreator
from data.datasets.dataset_role import DatasetRole
from data.datasets.trainer_dataset_manager import TrainerDatasetManager
from data.processing.abstract_data_processing_step import AbstractDataProcessingStep
from data.tree.artifact import Artifact
from data.tree.trace_link import TraceLink
from jobs.components.job_result import JobResult
from test.base_test import BaseTest


class BaseTraceTest(BaseTest):
    SOURCE_LAYERS = [{"s1": "s_token1",
                      "s2": "s_token2",
                      "s3": "s_token3"},
                     {"s4": "s_token4",
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
    _EXAMPLE_PREDICTIONS = np.array([0.6,
                                     0.4,
                                     0.3,
                                     0.8,
                                     0.1,
                                     0.01,
                                     0.2,
                                     0.4,
                                     0.4])
    _EXAMPLE_LABEL_IDS = np.array([1, 0, 0, 1, 0, 0, 0, 1, 0])
    EXAMPLE_PREDICTION_OUTPUT = PredictionOutput(predictions=_EXAMPLE_PREDICTIONS,
                                                 label_ids=_EXAMPLE_LABEL_IDS,
                                                 metrics=_EXAMPLE_METRIC_RESULTS)
    EXAMPLE_TRAINING_OUTPUT = {'global_step': 3, 'training_loss': 0.6927204132080078,
                               'metrics': {'train_runtime': 0.1516, 'train_samples_per_second': 79.13,
                                           'train_steps_per_second': 19.782, 'train_loss': 0.6927204132080078,
                                           'epoch': 3.0},
                               'status': 0}
    _EXAMPLE_PREDICTION_LINKS = {'source': 0, 'target': 1, 'score': 0.5}
    _EXAMPLE_PREDICTION_METRICS = {'test_loss': 0.6948729753494263, 'test_runtime': 0.0749,
                                   'test_samples_per_second': 240.328, 'test_steps_per_second': 40.055}
    _KEY_ERROR_MESSAGE = "{} not in {}"
    _VAL_ERROR_MESSAGE = "{} with value {} does not equal expected value of {} {}"
    _LEN_ERROR = "Length of {} does not match expected"

    _DATASET_PARAMS = {"source_layers": SOURCE_LAYERS,
                       "target_layers": TARGET_LAYERS,
                       "true_links": POS_LINKS}
    DATASET_ARGS_PARAMS = {
        "validation_percentage": VALIDATION_PERCENTAGE_DEFAULT
    }

    TRACE_ARGS_PARAMS = {
        "num_train_epochs": 1,
        "metrics": ["accuracy", "map_at_k"]
    }

    dataset_creator_definition = {
        "objectType": "CLASSIC",
        "source_layers": SOURCE_LAYERS,
        "target_layers": TARGET_LAYERS,
        "true_links": POS_LINKS
    }

    dataset_manager_definition = {
        "train_dataset_creator": dataset_creator_definition
    }

    model_manager_definition = {
        "model_path": "bert-base-uncased"
    }

    @staticmethod
    def create_dataset(dataset_role: DatasetRole,
                       dataset_creator_class: SupportedDatasetCreator = SupportedDatasetCreator.CLASSIC_TRACE,
                       dataset_creator_params: Dict = None,
                       include_links=True,
                       include_pre_processing: bool = False,
                       pre_processing_steps: List[AbstractDataProcessingStep] = None,
                       **kwargs
                       ) -> Dict[DatasetRole, AbstractDatasetCreator]:
        if not dataset_creator_params:
            dataset_creator_params = deepcopy(BaseTraceTest._DATASET_PARAMS)
        if not include_links:
            dataset_creator_params.pop("true_links")
        if not pre_processing_steps:
            dataset_creator_params["data_cleaner"] = BaseTest.DATA_CLEANER
        if include_pre_processing:
            dataset_creator_params["data_cleaner"] = BaseTest.DATA_CLEANER
        abstract_dataset = dataset_creator_class.value(**dataset_creator_params, **kwargs)
        return {dataset_role: abstract_dataset}

    @staticmethod
    def create_trainer_dataset_manager(dataset_map: Dict[DatasetRole, AbstractDatasetCreator],
                                       split_train_dataset=True) -> TrainerDatasetManager:
        if split_train_dataset:
            dataset_map[DatasetRole.VAL] = SplitDatasetCreator(val_percentage=VALIDATION_PERCENTAGE_DEFAULT)
        return TrainerDatasetManager.create_from_map(dataset_map)

    def assert_prediction_output_matches_expected(self, output: dict, threshold: int = 0.05):
        if JobResult.PREDICTIONS not in output:
            self.fail(self._KEY_ERROR_MESSAGE.format(JobResult.PREDICTIONS, output))
        predictions = output[JobResult.PREDICTIONS]
        if len(predictions) != len(self.ALL_TEST_LINKS):
            self.fail(self._LEN_ERROR.format(JobResult.PREDICTIONS))
        expected_links = {link for link in self.ALL_TEST_LINKS}
        predicted_links = set()
        for link_dict in output[JobResult.PREDICTIONS]:
            link = [None, None]
            for key, val in self._EXAMPLE_PREDICTION_LINKS.items():
                if key not in link_dict:
                    self.fail(self._KEY_ERROR_MESSAGE.format(key, JobResult.PREDICTIONS))
                if key == "score":
                    expected_val = self._EXAMPLE_PREDICTION_LINKS["score"]
                    if abs(val - expected_val) >= threshold:
                        self.fail(
                            self._VAL_ERROR_MESSAGE.format(key, val, expected_val, JobResult.PREDICTIONS))
                else:
                    link[val] = link_dict[key]
            predicted_links.add(tuple(link))
        self.assert_lists_have_the_same_vals(expected_links, predicted_links)
        if JobResult.METRICS not in output:
            self.fail(self._KEY_ERROR_MESSAGE.format(JobResult.METRICS, output))
        for metric in self._EXAMPLE_PREDICTION_METRICS.keys():
            if metric not in output[JobResult.METRICS]:
                self.fail(
                    self._KEY_ERROR_MESSAGE.format(JobResult.METRICS, output[JobResult.METRICS]))

    def assert_training_output_matches_expected(self, output_dict: dict):
        for key, value in self.EXAMPLE_TRAINING_OUTPUT.items():
            self.assertIn(key, output_dict)

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

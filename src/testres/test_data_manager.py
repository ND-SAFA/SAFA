from typing import List, Tuple, Union

import numpy as np
from transformers.trainer_utils import PredictionOutput

from data.tree.artifact import Artifact
from data.tree.trace_link import TraceLink


class TestDataManager:
    class Keys:
        ARTIFACTS = "artifacts"
        SOURCE = "source"
        TARGET = "target"
        TRACES = "traces"

    DATA = {
        Keys.ARTIFACTS: {
            Keys.SOURCE: [{"s1": "s_token1",
                           "s2": "s_token2",
                           "s3": "s_token3"},
                          {"s4": "s_token4",
                           "s5": "s_token5",
                           "s6": "s_token6"}],
            Keys.TARGET: [{"t1": "t_token1",
                           "t2": "t_token2",
                           "t3": "t_token3"},
                          {"t4": "t_token4",
                           "t5": "t_token5",
                           "t6": "t_token6"}]
        },
        Keys.TRACES: [("s1", "t1"), ("s2", "t1"), ("s3", "t2"), ("s4", "t4"), ("s4", "t5"), ("s5", "t6")]
    }
    LINKED_TARGETS = ["t1", "t2", "t4", "t5", "t6"]

    _EXAMPLE_METRIC_RESULTS = {'test_loss': 0.6929082870483398}
    _EXAMPLE_PREDICTIONS = np.array(
        [0.6, 0.4, 0.3, 0.8, 0.1, 0.01, 0.2, 0.4, 0.4])
    _EXAMPLE_LABEL_IDS = np.array([1, 0, 0, 1, 0, 0, 0, 1, 0])
    EXAMPLE_PREDICTION_OUTPUT = PredictionOutput(predictions=_EXAMPLE_PREDICTIONS,
                                                 label_ids=_EXAMPLE_LABEL_IDS,
                                                 metrics=_EXAMPLE_METRIC_RESULTS)
    EXAMPLE_TRAINING_OUTPUT = {'global_step': 3, 'training_loss': 0.6927204132080078,
                               'metrics': {'train_runtime': 0.1516, 'train_samples_per_second': 79.13,
                                           'train_steps_per_second': 19.782, 'train_loss': 0.6927204132080078,
                                           'epoch': 3.0},
                               'status': 0}
    EXAMPLE_PREDICTION_LINKS = {'source': 0, 'target': 1, 'score': 0.5}
    EXAMPLE_PREDICTION_METRICS = {'test_loss': 0.6948729753494263, 'test_runtime': 0.0749,
                                  'test_samples_per_second': 240.328, 'test_steps_per_second': 40.055}

    @staticmethod
    def get_all_links() -> List[Tuple[str, str]]:
        sources = TestDataManager.get_path([TestDataManager.Keys.ARTIFACTS, TestDataManager.Keys.SOURCE])
        targets = TestDataManager.get_path([TestDataManager.Keys.ARTIFACTS, TestDataManager.Keys.TARGET])
        links = []
        for source_dict, target_dict in zip(sources, targets):
            for source_id, source_body in source_dict.items():
                for target_id, target_body in target_dict.items():
                    links.append((source_id, target_id))
        return links

    @staticmethod
    def get_positive_links():
        return TestDataManager.get_path(TestDataManager.Keys.TRACES)

    @staticmethod
    def get_negative_links():
        all_links = TestDataManager.get_all_links()
        pos_links = TestDataManager.get_positive_links()
        return set(all_links).difference(set(pos_links))

    @staticmethod
    def get_linked_targets():
        return [link[1] for link in TestDataManager.get_positive_links()]

    @staticmethod
    def get_path(paths: Union[List[str], str], data=None):
        """
        Returns the data at given JSON path.
        :param paths: List of strings representings keys to index.
        :param data: The current data accumulator.
        :return: The data found at keys.
        """
        if isinstance(paths, str):
            return TestDataManager.get_path([paths])
        if len(paths) == 0:
            return data
        if data:
            export_data = data[paths[0]]
        else:
            export_data = TestDataManager.DATA[paths[0]]
        return TestDataManager.get_path(paths[1:], export_data)

    @staticmethod
    def get_positive_link_ids() -> List[int]:
        positive_links = TestDataManager.get_positive_links()
        return TestDataManager._get_link_ids(positive_links)

    @staticmethod
    def get_all_link_ids() -> List[int]:
        all_links = TestDataManager.get_all_links()
        return TestDataManager._get_link_ids(all_links)

    @staticmethod
    def get_negative_link_ids() -> List[int]:
        negative_links = TestDataManager.get_negative_links()
        return TestDataManager._get_link_ids(negative_links)

    @staticmethod
    def _get_link_ids(links_list):
        return list(TestDataManager._create_link_map(links_list).keys())

    @staticmethod
    def _create_link_map(link_list):
        links = {}
        for source, target in link_list:
            link = TestDataManager._create_test_link(source, target)
            links[link.id] = link
        return links

    @staticmethod
    def _create_test_link(source: str, target: str):
        s = Artifact(source, TestDataManager._get_artifact_body(source))
        t = Artifact(target, TestDataManager._get_artifact_body(target))
        return TraceLink(s, t)

    @staticmethod
    def _create_test_artifact(artifacts_dict):
        return [Artifact(id_, token) for id_, token in artifacts_dict.items()]

    @staticmethod
    def _get_artifact_body(artifact_id: str):
        for artifact_type_key in [TestDataManager.Keys.SOURCE, TestDataManager.Keys.TARGET]:
            artifact_levels = TestDataManager.get_path([TestDataManager.Keys.ARTIFACTS, artifact_type_key])
            for artifact_level in artifact_levels:
                if artifact_id in artifact_level:
                    return artifact_level[artifact_id]
        raise ValueError("Could not find artifact with id:" + artifact_id)

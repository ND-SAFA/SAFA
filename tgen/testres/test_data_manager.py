from typing import Dict, List, Union

import numpy as np
from transformers.trainer_utils import PredictionOutput

from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame, ArtifactKeys
from tgen.data.dataframes.trace_dataframe import TraceDataFrame


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
        [[0.4, 0.6], [0.6, 0.4], [0.7, 0.3], [0.2, 0.8], [0.9, 0.1], [0.99, 0.01], [0.8, 0.2], [0.6, 0.4], [0.6, 0.4],
         [0.4, 0.6], [0.6, 0.4], [0.7, 0.3], [0.2, 0.8], [0.9, 0.1], [0.99, 0.01], [0.8, 0.2], [0.6, 0.4], [0.6, 0.4]])
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
    EXAMPLE_PREDICTION_METRICS = {'map': 0.6948729753494263, 'global_ap': 0.0749}

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
    def create_artifact_dataframe():
        sources = TestDataManager.get_path([TestDataManager.Keys.ARTIFACTS, TestDataManager.Keys.SOURCE])
        targets = TestDataManager.get_path([TestDataManager.Keys.ARTIFACTS, TestDataManager.Keys.TARGET])
        artifact_df = ArtifactDataFrame()
        for layer_num, layer_sources in enumerate(sources):
            for s_id, s_body in layer_sources.items():
                artifact_df.add_artifact(s_id, s_body, layer_num)
        for layer_num, layer_targets in enumerate(targets):
            for t_id, t_body in layer_targets.items():
                artifact_df.add_artifact(t_id, t_body, layer_num)
        return artifact_df

    @staticmethod
    def create_trace_dataframe(link_list):
        trace_df = TraceDataFrame()
        for source, target in link_list:
            link = TestDataManager._create_test_link(trace_df, source, target)
        return trace_df

    @staticmethod
    def _create_test_link(trace_dataframe: TraceDataFrame, source: str, target: str):
        return trace_dataframe.add_link(source, target)

    @staticmethod
    def _create_test_artifact(artifacts_dict):
        artifacts = {ArtifactKeys.ID.value: [], ArtifactKeys.CONTENT.value: [], ArtifactKeys.LAYER_ID.value: []}
        for id_, token in artifacts_dict.items():
            artifacts[ArtifactKeys.ID.value].append(id_)
            artifacts[ArtifactKeys.CONTENT.value].append(token)
            artifacts[ArtifactKeys.LAYER_ID.value].append(1)
        return artifacts

    @staticmethod
    def _get_artifact_body(artifact_id: str):
        """
        :param artifact_id: The id of the artifact whose body is returned.
        :return: Returns the body of the artifact with given id.
        """
        artifact_map = TestDataManager.get_artifact_map()
        if artifact_id in artifact_map:
            return artifact_map[artifact_id]
        raise ValueError("Could not find artifact with id:" + artifact_id)

    @staticmethod
    def get_artifact_map() -> Dict[str, str]:
        """
        :return: map between artifact id to its body.
        """
        artifacts = {}
        for artifact_type_key in [TestDataManager.Keys.SOURCE, TestDataManager.Keys.TARGET]:
            artifact_levels = TestDataManager.get_path([TestDataManager.Keys.ARTIFACTS, artifact_type_key])
            for artifact_level in artifact_levels:
                for artifact_id, artifact_body in artifact_level.items():
                    artifacts[artifact_id] = artifact_body
        return artifacts

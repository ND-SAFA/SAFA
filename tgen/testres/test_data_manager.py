from typing import Dict, List, Union

import numpy as np
from transformers.trainer_utils import PredictionOutput

from tgen.common.objects.artifact import Artifact
from tgen.common.objects.trace import Trace
from tgen.common.objects.trace_layer import TraceLayer
from common_resources.data.dataframes.artifact_dataframe import ArtifactDataFrame
from common_resources.data.dataframes.trace_dataframe import TraceDataFrame
from common_resources.data.keys.structure_keys import ArtifactKeys
from common_resources.data.readers.api_project_reader import ApiProjectReader
from common_resources.data.readers.definitions.api_definition import ApiDefinition


class TestDataManager:
    class Keys:
        ARTIFACTS = "artifacts"
        SOURCE = "source"
        TARGET = "target"
        TRACES = "traces"
        LAYERS = "LAYERS"

    DATA = {
        Keys.ARTIFACTS: {
            "source_1": {"s1": "s_token1",
                         "s2": "s_token2",
                         "s3": "s_token3"},
            "source_2": {"s4": "s_token4",
                         "s5": "s_token5",
                         "s6": "s_token6"},
            "target_1": {"t1": "t_token1",
                         "t2": "t_token2",
                         "t3": "t_token3"},
            "target_2": {"t4": "t_token4",
                         "t5": "t_token5",
                         "t6": "t_token6"}
        },
        Keys.LAYERS: [{"parent": "target_1", "child": "source_1"},
                      {"parent": "target_2", "child": "source_2"}],
        Keys.TRACES: [{"source": "s1", "target": "t1", "label": 1},
                      {"source": "s2", "target": "t1", "label": 1},
                      {"source": "s3", "target": "t2", "label": 1},
                      {"source": "s4", "target": "t4", "label": 1},
                      {"source": "s4", "target": "t5", "label": 1},
                      {"source": "s5", "target": "t6", "label": 1}]
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
        artifacts = TestDataManager.get_path([TestDataManager.Keys.ARTIFACTS])
        artifact_df = ArtifactDataFrame()
        for artifact_type, artifacts in artifacts.items():
            for artifact_id, artifact_body in artifacts.items():
                artifact_df.add_artifact(artifact_id, artifact_body, artifact_type)

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
    def get_artifact_body(artifact_id: str):
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
        artifact_map = {}
        artifact_levels = TestDataManager.get_path([TestDataManager.Keys.ARTIFACTS])
        for level_name, level_map in artifact_levels.items():
            for artifact_id, artifact_body in level_map.items():
                artifact_map[artifact_id] = artifact_body
        return artifact_map

    @staticmethod
    def get_project_reader() -> ApiProjectReader:
        layers = [TraceLayer(**params) for params in TestDataManager.get_path(TestDataManager.Keys.LAYERS)]
        links = [Trace(**params) for params in TestDataManager.get_path(TestDataManager.Keys.TRACES)]
        api_definition = ApiDefinition(
            artifacts=TestDataManager.get_artifacts(),
            layers=layers,
            links=links
        )
        return ApiProjectReader(api_definition=api_definition)

    @classmethod
    def get_n_candidates(cls) -> int:
        """
        :return: Returns the number of candidates in dataset.
        """
        artifacts = cls.DATA[cls.Keys.ARTIFACTS]
        layers = cls.DATA[cls.Keys.LAYERS]
        n_candidates_total = 0
        for trace_layer in layers:
            parent_type, child_type = trace_layer["parent"], trace_layer["child"]

            parent_artifacts = artifacts[parent_type]
            child_artifacts = artifacts[child_type]
            n_candidates = len(parent_artifacts) * len(child_artifacts)
            n_candidates_total += n_candidates
        return n_candidates_total

    @classmethod
    def get_artifacts(cls) -> List[Artifact]:
        artifacts = []
        for artifact_type, artifacts_in_type in TestDataManager.DATA[TestDataManager.Keys.ARTIFACTS].items():
            for artifact_id, artifact_body in artifacts_in_type.items():
                artifact = Artifact(id=artifact_id, content=artifact_body, layer_id=artifact_type, summary=None)
                artifacts.append(artifact)
        return artifacts

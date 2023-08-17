from copy import deepcopy
from typing import Any, Dict, List, Tuple

from tgen.common.artifact import Artifact
from tgen.core.trace_output.trace_prediction_output import TracePredictionEntry
from tgen.data.keys.structure_keys import StructuredKeys
from tgen.ranking.common.trace_layer import TraceLayer
from tgen.testres.test_data_manager import TestDataManager

ArtifactInstruction = Tuple[Any, str]
LayerInstruction = List[ArtifactInstruction]
Entry = Dict
LayerEntry = List[Entry]
TraceInstruction = Tuple


class EntryCreator:
    """
    Responsible for creating project entity entries for testing.s
    """

    @staticmethod
    def create_trace_entries(trace_artifact_ids: List[TraceInstruction]):
        """
        Generates trace entries between artifact in each entry.
        :param trace_artifact_ids: The artifacts ids to create link for.
        :return: List of trace entries.
        """

        return [EntryCreator.create_trace_entry(params) for params in trace_artifact_ids]

    @staticmethod
    def create_trace_entry(params: TraceInstruction):
        """
        Creates a trace entry with optional labels.
        :param params: Tuple consisting of source id, target id, and optionally the label.
        :return: List of trace entries.
        """
        entry = {StructuredKeys.Trace.SOURCE.value: params[0], StructuredKeys.Trace.TARGET.value: params[1]}
        if len(params) == 3:
            entry[StructuredKeys.Trace.LABEL.value] = params[2]
        return entry

    @staticmethod
    def create_layer_mapping_entries(layer_mappings: List[ArtifactInstruction]) -> List[TraceLayer]:
        """
        Creates layer mapping in structured dataset format.
        :param layer_mappings: List of source and target types to map together.
        :return: List of layer mapping entries.
        """
        return [TraceLayer(child=s_type, parent=t_type) for s_type, t_type in layer_mappings]

    @staticmethod
    def get_entries_in_type(type_key: TestDataManager.Keys, layers_to_include: List[int] = None) -> List[Artifact]:
        """
        Returns entries associated with type existing in data manager.
        :param type_key: The key to access artifacts in artifact type.
        :param layers_to_include: The layers to filter artifacts by.
        :return: List of entries.
        """
        artifact_data = EntryCreator.read_artifact_layers(type_key, layers_to_include)
        return EntryCreator.create_artifact_entries(artifact_data)

    @staticmethod
    def read_artifact_layers(type_key: TestDataManager.Keys, layer_indices: List[int] = None) -> List[LayerInstruction]:
        """
        Extracts the artifact data associated with type.
        :param type_key: The key referring to source or target artifacts.
        :param layer_indices: The set of artifacts within type to extract. If none, all sets are used.
        :return: Data used to create entries using EntryCreator.
        """
        key_map = "child" if "source" == type_key else "parent"
        artifact_layer_map = TestDataManager.get_path([TestDataManager.Keys.ARTIFACTS])
        traced_layers = TestDataManager.get_path([TestDataManager.Keys.LAYERS])
        entries = []
        for layer_index, traced_layer in enumerate(traced_layers):
            layer_name = traced_layer[key_map]
            layer_artifacts = artifact_layer_map[layer_name]
            layer_entries = []
            for artifact in layer_artifacts.items():
                layer_entries.append(artifact)
            entries.append(layer_entries)
        return deepcopy(entries)

    @staticmethod
    def create_artifact_entries(artifact_layers: List[Dict[str, str]]) -> List[Artifact]:
        """
        Creates artifact entries by extracting id and body from items.
        :param artifact_layers: Items containing artifact ids and body per layer.
        :return: artifact entries created.
        """
        artifacts = []
        for artifact_items in artifact_layers:
            for a_id, a_body in artifact_items:
                artifacts.append(Artifact(id=id, content=a_body))
        return artifacts

    @staticmethod
    def create_trace_predictions(n_parents: int, n_children: int, scores: List[float] = None, labels: List[float] = None) -> List[
        TracePredictionEntry]:
        """
        Creates trace
        :param n_parents: The number of parents to create.
        :param n_children: The number of children to create.
        :param scores: The scores to assign to entries (in parent-children order)
        :param labels: The labels to assign to entries (in parent-children order)
        :return: List of trace predictions.
        """
        i = 0
        entries = []
        for p_id in range(n_parents):
            for c_id in range(n_children):
                entry = TracePredictionEntry(
                    source=f"c{c_id}",
                    target=f"p{p_id}",
                    score=None,
                    label=None,
                    explanation=None
                )
                if scores:
                    entry["score"] = scores[i]
                if labels:
                    entry["label"] = labels[i]
                entries.append(entry)
                i += 1
        return entries

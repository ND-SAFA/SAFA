from copy import deepcopy
from typing import Any, Dict, List, Tuple

from data.keys.structure_keys import StructuredKeys
from testres.test_data_manager import TestDataManager

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
        entry = {StructuredKeys.Trace.SOURCE: params[0], StructuredKeys.Trace.TARGET: params[1]}
        if len(params) == 3:
            entry[StructuredKeys.Trace.LABEL] = params[2]
        return entry

    @staticmethod
    def create_layer_mapping_entries(layer_mappings: List[ArtifactInstruction]) -> LayerEntry:
        """
        Creates layer mapping in structured dataset format.
        :param layer_mappings: List of source and target types to map together.
        :return: List of layer mapping entries.
        """
        return [{StructuredKeys.LayerMapping.SOURCE_TYPE: s_type,
                 StructuredKeys.LayerMapping.TARGET_TYPE: t_type}
                for s_type, t_type in layer_mappings]

    @staticmethod
    def get_entries_in_type(type_key: TestDataManager.Keys, layers_to_include: List[int] = None) -> List[LayerEntry]:
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

        entries = []
        for layer_index, artifact_layer in enumerate(TestDataManager.DATA[TestDataManager.Keys.ARTIFACTS][type_key]):
            layer_entries = []
            if layer_indices is not None:
                if layer_index not in layer_indices:
                    continue
            for a_id, a_body in artifact_layer.items():
                layer_entries.append((a_id, a_body))
            entries.append(layer_entries)
        return deepcopy(entries)

    @staticmethod
    def create_artifact_entries(artifact_layers: List[LayerInstruction]) -> List[List[Entry]]:
        """
        Creates artifact entries by extracting id and body from items.
        :param artifact_layers: Items containing artifact ids and body per layer.
        :return: artifact entries created.
        """
        return [
            [{
                StructuredKeys.Artifact.ID: a_id,
                StructuredKeys.Artifact.BODY: a_body
            } for a_id, a_body in artifact_items] for artifact_items in artifact_layers]

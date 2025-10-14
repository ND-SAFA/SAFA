from typing import Any, Dict, List, Tuple

from gen_common.data.objects.artifact import Artifact
from gen_common.data.objects.trace import Trace
from gen_common.data.keys.structure_keys import StructuredKeys
from gen_common_test.test_data.test_data_manager import TestDataManager
from gen_common.data.objects.trace_layer import TraceLayer

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
        artifacts = TestDataManager.get_artifacts()
        layer_artifacts = [a for a in artifacts if a["layer_id"] == type_key]
        return layer_artifacts

    @staticmethod
    def create_trace_predictions(n_parents: int, n_children: int, scores: List[float] = None, labels: List[float] = None) -> List[
        Trace]:
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
                entry = Trace(
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

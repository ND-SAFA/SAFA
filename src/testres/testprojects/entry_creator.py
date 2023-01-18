from typing import Any, Dict, List, Tuple

from data.datasets.keys.structure_keys import StructureKeys
from testres.test_data_manager import TestDataManager


class EntryCreator:
    """
    Responsible for creating project entity entries for testing.s
    """

    @staticmethod
    def create_artifact_entries(artifact_items: List[Tuple[Any, str]]):
        """
        Creates artifact entries by extracting id and body from items.
        :param artifact_items: Items containing artifact ids and body.
        :return: artifact entries created.
        """
        return [{
            StructureKeys.Artifact.ID: a_id,
            StructureKeys.Artifact.BODY: a_body
        } for a_id, a_body in artifact_items]

    @staticmethod
    def create_trace_entries(trace_artifact_ids: List[Tuple]):
        """
        Generates trace entries between artifact in each entry.
        :param trace_artifact_ids: The artifacts ids to create link for.
        :return: List of trace entries.
        """

        return [EntryCreator.create_trace_entry(params) for params in trace_artifact_ids]

    @staticmethod
    def create_trace_entry(params: Tuple):
        """
        Creates a trace entry with optional labels.
        :param params: Tuple consisting of source id, target id, and optionally the label.
        :return: List of trace entries.
        """
        entry = {}
        entry[StructureKeys.Trace.SOURCE] = params[0]
        entry[StructureKeys.Trace.TARGET] = params[1]
        if len(params) == 3:
            entry[StructureKeys.Trace.LABEL] = params[2]
        return entry

    @staticmethod
    def create_layer_mapping_entries(layer_mappings: List[Tuple[str, str]]) -> List[Dict]:
        """
        Creates layer mapping in structured dataset format.
        :param layer_mappings: List of source and target types to map together.
        :return: List of layer mapping entries.
        """
        return [{StructureKeys.LayerMapping.SOURCE_TYPE: s_type,
                 StructureKeys.LayerMapping.TARGET_TYPE: t_type}
                for s_type, t_type in layer_mappings]

    @staticmethod
    def get_entries_in_type(type_key: TestDataManager.Keys, **kwargs) -> List[Dict]:
        """
        Returns entries associated with type existing in data manager.
        :param type_key: The key to access artifacts in artifact type.
        :param kwargs: Additional arguments passed to reader.
        :return: List of entries.
        """
        artifact_data = EntryCreator.read_artifacts_in_type(type_key, **kwargs)
        return EntryCreator.create_artifact_entries(artifact_data)

    @staticmethod
    def read_artifacts_in_type(type_key: TestDataManager.Keys, artifact_set_indices: List[int] = None) -> List[Tuple[str, str]]:
        """
        Extracts the artifact data associated with type.
        :param type_key: The key referring to source or target artifacts.
        :param artifact_set_indices: The set of artifacts within type to extract. If none, all sets are used.
        :return: Data used to create entries using EntryCreator.
        """

        entries = []
        for i, artifact_set in enumerate(TestDataManager.DATA[TestDataManager.Keys.ARTIFACTS][type_key]):
            if artifact_set_indices is not None:
                if i not in artifact_set_indices:
                    continue
            for a_id, a_body in artifact_set.items():
                entries.append((a_id, a_body))
        return entries

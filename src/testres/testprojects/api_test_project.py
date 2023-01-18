from typing import Dict, List

from data.datasets.creators.readers.api_project_reader import ApiProjectReader
from data.datasets.keys.structure_keys import StructureKeys
from testres.test_data_manager import TestDataManager
from testres.testprojects.csv_test_project import CsvTestProject
from testres.testprojects.entry_creator import EntryCreator


class ApiTestProject(CsvTestProject):
    """
    Contains entries for classic trace project.
    """

    @property
    def project_path(self) -> str:
        raise ValueError("Classic trace does not contain project path.")

    def get_trace_entries(self) -> List[Dict]:
        trace_data = TestDataManager.DATA[TestDataManager.Keys.TRACES]
        trace_data = [(a_id, a_body, 1) for a_id, a_body in trace_data]
        return EntryCreator.create_trace_entries(trace_data)

    def get_layer_mapping_entries(self) -> List[Dict]:
        layer_mapping_data = [
            (
                ApiProjectReader.create_layer_id(StructureKeys.LayerMapping.SOURCE_TYPE, 0),
                ApiProjectReader.create_layer_id(StructureKeys.LayerMapping.TARGET_TYPE, 0)
            ),
            (
                ApiProjectReader.create_layer_id(StructureKeys.LayerMapping.SOURCE_TYPE, 1),
                ApiProjectReader.create_layer_id(StructureKeys.LayerMapping.TARGET_TYPE, 1)
            )
        ]
        return EntryCreator.create_layer_mapping_entries(layer_mapping_data)

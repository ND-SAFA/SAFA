from typing import Dict, List

from testres.paths.project_paths import STRUCTURE_PROJECT_PATH
from testres.testprojects.abstract_test_project import AbstractTestProject
from testres.testprojects.entry_creator import EntryCreator, LayerEntry, LayerInstruction


class StructuredTestProject(AbstractTestProject):

    @property
    def project_path(self) -> str:
        return STRUCTURE_PROJECT_PATH

    def get_trace_entries(self) -> List[Dict]:
        trace_data = [(1674, 80), (1674, 85), (1688, 142), (1688, 205)]
        return EntryCreator.create_trace_entries(trace_data)

    def get_layer_mapping_entries(self) -> List[Dict]:
        return EntryCreator.create_layer_mapping_entries([
            ("Requirements", "Regulatory Codes")
        ])

    @staticmethod
    def get_source_entries() -> List[LayerEntry]:
        source_artifact_layer: LayerInstruction = [
            (1674, "The system shall improve accessibility of online clinical information and results."),
            (1688,
             "The system shall integrate all components of the patient record to provide comprehensive and intelligent clinical information access and reporting.")
        ]
        return EntryCreator.create_artifact_entries([source_artifact_layer])

    @staticmethod
    def get_target_entries() -> List[LayerEntry]:
        target_artifact_layer = [
            (80, "The system shall provide protection to maintain the integrity of clinical data during concurrent access."),
            (85, "The system shall provide the ability for a user to whom a result is presented to acknowledge the result."),
            (142,
             "The system shall provide the ability to create hardcopy and electronic report summary information (procedures, medications, labs, immunizations, allergies, and vital signs)."),
            (205,
             "The system shall provide the ability to generate reports consisting of all or part of an individual patient?s medical record (e.g. patient summary).")
        ]
        return EntryCreator.create_artifact_entries([target_artifact_layer])

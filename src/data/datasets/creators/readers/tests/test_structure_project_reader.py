import os

from data.datasets.creators.readers.definitions.structure_project_definition import StructureProjectDefinition
from testres.base_test import BaseTest
from testres.paths.paths import TEST_DATA_DIR
from testres.test_assertions import TestAssertions


class TestStructureProjectReader(BaseTest):
    PROJECT_PATH = os.path.join(TEST_DATA_DIR, "structure")
    ARTIFACT_FILES = ["source.xml", "target.xml"]
    TRACE_FILES = ["answer.txt"]

    def test_get_artifact_definitions(self):
        structure_project_reader = StructureProjectDefinition(self.PROJECT_PATH)
        artifact_definitions = structure_project_reader.get_artifact_definitions()
        TestAssertions.assert_file_definitions_have_files(self, artifact_definitions, self.ARTIFACT_FILES)

    def test_get_trace_definitions(self):
        structure_project_reader = StructureProjectDefinition(self.PROJECT_PATH)
        trace_definitions = structure_project_reader.get_trace_definitions()
        TestAssertions.assert_file_definitions_have_files(self, trace_definitions, self.TRACE_FILES)

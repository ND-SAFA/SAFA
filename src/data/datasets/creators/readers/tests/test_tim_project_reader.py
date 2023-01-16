import os

from data.datasets.creators.readers.definitions.tim_project_definition import TimProjectDefinition
from testres.base_test import BaseTest
from testres.paths.paths import TEST_DATA_DIR
from testres.test_assertions import TestAssertions


class TestTimProjectReader(BaseTest):
    PROJECT_PATH = os.path.join(TEST_DATA_DIR, "safa")
    ARTIFACT_FILES = ["Layer1Source.json", "Layer1Target.json", "Layer2Source.json", "Layer2Target.json"]
    TRACE_FILES = ["Layer1Source2Target.json", "Layer2Source2Target.json"]
    BASE_PATH = "abc/def/hello"

    def test_get_artifact_definition(self):
        tim_project_reader = TimProjectDefinition(self.PROJECT_PATH)
        artifact_definitions = tim_project_reader.get_artifact_definitions()
        TestAssertions.assert_file_definitions_have_files(self, artifact_definitions, self.ARTIFACT_FILES)

    def test_get_trace_definitions(self):
        tim_project_reader = TimProjectDefinition(self.PROJECT_PATH)
        trace_definitions = tim_project_reader._create_trace_definitions()
        TestAssertions.assert_file_definitions_have_files(self, trace_definitions, self.TRACE_FILES)

    def test_get_file_format_supported(self):
        supported_format_extensions = [".csv", ".json"]

        for file_extension in supported_format_extensions:
            file_path = self.BASE_PATH + file_extension
            file_type = TimProjectDefinition.get_file_format(file_path)
            self.assertIn(file_type, file_extension)

    def test_get_file_format_unsupported(self):
        unsupported_formats = [".xml", ".jpeg"]
        for file_extension in unsupported_formats:
            file_path = self.BASE_PATH + file_extension

            def attempt():
                TimProjectDefinition.get_file_format(file_path)

            self.assertRaises(ValueError, attempt)

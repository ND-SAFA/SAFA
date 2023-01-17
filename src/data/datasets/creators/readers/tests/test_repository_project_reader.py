import os

from data.datasets.creators.readers.definitions.repository_project_definition import RepositoryProjectDefinition
from data.datasets.keys.safa_format import SafaKeys
from testres.base_test import BaseTest
from testres.paths.paths import TEST_DATA_DIR
from testres.test_assertions import TestAssertions


class TestRepositoryProjectReader(BaseTest):
    PROJECT_PATH = os.path.join(TEST_DATA_DIR, "repo")
    ARTIFACT_FILES = ["commit.csv", "issue.csv"]
    TRACE_FILES = ["commit2issue.csv"]

    def test_read_definition(self):
        repository_project_reader = RepositoryProjectDefinition(self.PROJECT_PATH)
        definition = repository_project_reader.definition
        # VP 1. Verify artifact files
        artifact_definitions = definition[SafaKeys.DATAFILES_KEY]
        TestAssertions.assert_file_definitions_have_files(self, artifact_definitions, self.ARTIFACT_FILES)

        # VP 2. Verify trace files
        definition.pop(SafaKeys.DATAFILES_KEY)
        trace_definitions = definition
        TestAssertions.assert_file_definitions_have_files(self, trace_definitions, self.TRACE_FILES)

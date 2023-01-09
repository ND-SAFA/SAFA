import os
from typing import Dict

from data.datasets.creators.readers.entity.artifact_reader import ArtifactReader
from data.datasets.creators.readers.entity.trace_entity_reader import TraceEntityReader
from data.datasets.keys.structure_keys import StructureKeys
from data.tree.trace_link import TraceLink
from testres.base_test import BaseTest
from testres.paths.paths import TEST_DATA_DIR
from util.file_util import FileUtil


class TestTraceEntityReader(BaseTest):
    """
    Tests that trace links are created, validated, and exported.
    """
    PROJECT_PATH = os.path.join(TEST_DATA_DIR, "test_errors", "trace_entity_reader")
    DEFINITION_PATH = os.path.join(PROJECT_PATH, "definition.json")
    PROJECT_DEFINITION = FileUtil.read_json_file(DEFINITION_PATH, as_uncased_dict=True)
    TRACE_DEFINITION = PROJECT_DEFINITION[StructureKeys.TRACES]["source2target"]
    ARTIFACT_TYPES = ["source", "target"]

    def test_missing_source(self):
        """
        Checks that default rules catches that trace link reference undefined source.
        """
        name2artifacts = self.create_artifact_reader()
        trace_entity_reader = TraceEntityReader(self.PROJECT_PATH, self.TRACE_DEFINITION, name2artifacts)
        with self.assertRaises(AssertionError) as e:
            trace_entity_reader.get_entities()
        self.assertIn("S2", e.exception.args[0])

    def test_missing_target(self):
        """
        Checks that allowing missing sources catches missing target in trace links.
        """
        name2artifacts = self.create_artifact_reader()
        trace_entity_reader = TraceEntityReader(self.PROJECT_PATH, self.TRACE_DEFINITION, name2artifacts, **{
            StructureKeys.OVERRIDES: {
                "ALLOW_MISSING_SOURCE": True
            }
        })
        with self.assertRaises(AssertionError) as e:
            trace_entity_reader.get_entities()
        self.assertIn("T2", e.exception.args[0])

    def test_ignore_missing_artifacts(self):
        """
        Tests that trace link is created if both missing sources and targets are ignored.
        """
        name2artifacts = self.create_artifact_reader()
        trace_entity_reader = TraceEntityReader(self.PROJECT_PATH, self.TRACE_DEFINITION, name2artifacts, **{
            StructureKeys.OVERRIDES: {
                "ALLOW_MISSING_SOURCE": True,
                "ALLOW_MISSING_TARGET": True
            }
        })
        id2trace: Dict[int, TraceLink] = trace_entity_reader.get_entities()
        self.assertEqual(len(id2trace), 1)
        trace: TraceLink = list(id2trace.values())[0]
        self.assertEqual(trace.source.id, "S1")
        self.assertEqual(trace.target.id, "T1")

    @staticmethod
    def create_artifact_reader() -> Dict[str, ArtifactReader]:
        """
        :return: Map between name of artifact type and its reader.
        """
        return {
            name: ArtifactReader(TestTraceEntityReader.PROJECT_PATH,
                                 TestTraceEntityReader.PROJECT_DEFINITION[StructureKeys.ARTIFACTS][name]) for name in
            TestTraceEntityReader.ARTIFACT_TYPES
        }

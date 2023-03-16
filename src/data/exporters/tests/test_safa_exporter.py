from unittest import skip

from data.creators.trace_dataset_creator import TraceDatasetCreator
from data.exporters.safa_exporter import SafaExporter
from data.readers.structured_project_reader import StructuredProjectReader
from testres.base_test import BaseTest
from testres.paths.paths import TEST_OUTPUT_DIR
from util.object_creator import ObjectCreator


class TestSafaExporter(BaseTest):
    """
    Tests the individual methods of the exporter .
    """

    def test_export(self):
        """
        Tests safa exporter by exporting to safa format and trying to read it again.
        """
        safa_exporter = SafaExporter()
        trace_dataset_creator = ObjectCreator.create(TraceDatasetCreator)
        artifact_df, trace_df, layer_mapping_df = trace_dataset_creator.project_reader.read_project()
        trace_dataset = trace_dataset_creator.create()
        safa_exporter.export(TEST_OUTPUT_DIR, trace_dataset.links, artifact_df, layer_mapping_df)

        project_reader = StructuredProjectReader(TEST_OUTPUT_DIR)
        other_artifact_df, other_trace_df, other_layer_mapping_df = project_reader.read_project()

        self.assertEqual(len(artifact_df), len(other_artifact_df))
        self.assertEqual(len(trace_df), len(other_trace_df))
        self.assertEqual(len(layer_mapping_df), len(layer_mapping_df))

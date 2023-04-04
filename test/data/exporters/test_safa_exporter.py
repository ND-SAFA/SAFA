from tgen.data.creators.trace_dataset_creator import TraceDatasetCreator
from tgen.data.exporters.safa_exporter import SafaExporter
from tgen.data.readers.structured_project_reader import StructuredProjectReader
from test.testres.base_test import BaseTest
from test.testres.paths.paths import TEST_OUTPUT_DIR
from test.testres.object_creator import ObjectCreator


class TestSafaExporter(BaseTest):
    """
    Tests the individual methods of the exporter .
    """

    def test_export(self):
        """
        Tests safa exporter by exporting to safa format and trying to read it again.
        """

        trace_dataset_creator = ObjectCreator.create(TraceDatasetCreator)
        safa_exporter = SafaExporter(TEST_OUTPUT_DIR, trace_dataset_creator)
        safa_exporter.export()

        project_creator = TraceDatasetCreator(StructuredProjectReader(TEST_OUTPUT_DIR))
        other_dataset = project_creator.create()

        self.assertEqual(len(safa_exporter._dataset.artifact_df), len(other_dataset.artifact_df))
        self.assertEqual(len(safa_exporter._dataset.trace_df), len(other_dataset.trace_df))
        self.assertEqual(len(safa_exporter._dataset.layer_mapping_df), len(other_dataset.layer_mapping_df))

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

        trace_dataset_creator = ObjectCreator.create(TraceDatasetCreator)
        safa_exporter = SafaExporter(TEST_OUTPUT_DIR, trace_dataset_creator)
        safa_exporter.export()

        project_creator = TraceDatasetCreator(StructuredProjectReader(TEST_OUTPUT_DIR))
        other_dataset = project_creator.create()

        self.assertEqual(len(safa_exporter.dataset.artifact_df), len(other_dataset.artifact_df))
        self.assertEqual(len(safa_exporter.dataset.trace_df), len(other_dataset.trace_df))
        self.assertEqual(len(safa_exporter.dataset.layer_mapping_df), len(other_dataset.layer_mapping_df))

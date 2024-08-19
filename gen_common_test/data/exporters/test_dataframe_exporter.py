from gen_common.data.creators.trace_dataset_creator import TraceDatasetCreator
from gen_common.data.exporters.dataframe_exporter import DataFrameExporter
from gen_common.data.readers.dataframe_project_reader import DataFrameProjectReader
from gen_common_test.base.object_definitions import TestObjectDefinitions
from gen_common_test.base.paths.base_paths import GEN_COMMON_TEST_OUTPUT_PATH
from gen_common_test.base.tests.base_test import BaseTest


class TestDataFrameExporter(BaseTest):
    """
    Tests the individual methods of the exporter .
    """

    def test_export(self):
        """
        Tests dataframe exporter by exporting to dataframe format and trying to read it again.
        """

        trace_dataset_creator = TestObjectDefinitions.create(TraceDatasetCreator)
        safa_exporter = DataFrameExporter(GEN_COMMON_TEST_OUTPUT_PATH, trace_dataset_creator)
        safa_exporter.export()

        reader = DataFrameProjectReader(GEN_COMMON_TEST_OUTPUT_PATH, overrides={'allowed_orphans': 2, 'remove_orphans': False})
        project_creator = TraceDatasetCreator(reader)
        other_dataset = project_creator.create()

        self.assertEqual(len(safa_exporter._dataset.artifact_df), len(other_dataset.artifact_df))
        self.assertEqual(len(safa_exporter._dataset.trace_df), len(other_dataset.trace_df))
        self.assertEqual(len(safa_exporter._dataset.layer_df), len(other_dataset.layer_df))

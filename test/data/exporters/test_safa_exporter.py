import os
from typing import List

from tgen.core.trace_output.trace_prediction_output import TracePredictionEntry
from tgen.data.creators.trace_dataset_creator import TraceDatasetCreator
from tgen.data.exporters.safa_exporter import SafaExporter
from tgen.data.readers.api_project_reader import ApiProjectReader
from tgen.data.readers.definitions.api_definition import ApiDefinition
from tgen.data.readers.structured_project_reader import StructuredProjectReader
from tgen.ranking.common.trace_layer import TraceLayer
from tgen.testres.base_tests.base_test import BaseTest
from tgen.testres.object_creator import ObjectCreator
from tgen.testres.paths.paths import TEST_OUTPUT_DIR


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
        self.assertEqual(len(safa_exporter._dataset.layer_df), len(other_dataset.layer_df))

    def test_export_generated_links(self):
        artifact_layers = {
            "source": {f"S{i}": "dummy text" for i in range(3)},
            "target": {f"T{i}": "dummy text" for i in range(3)}
        }
        layers: List[TraceLayer] = [TraceLayer(child="source", parent="target")]
        true_links: List[TracePredictionEntry] = [{
            "source": "S1",
            "target": "T2",
            "score": 0.4,
            "explanation": "EXPLANATION"
        }]
        api_definition = ApiDefinition(artifact_layers=artifact_layers, layers=layers, true_links=true_links)
        api_project_reader = ApiProjectReader(api_definition=api_definition)
        trace_dataset_creator = TraceDatasetCreator(project_reader=api_project_reader)
        safa_exporter = SafaExporter(TEST_OUTPUT_DIR, dataset_creator=trace_dataset_creator)
        safa_exporter.export()

        files = os.listdir(TEST_OUTPUT_DIR)
        print(files)
        print("hi")

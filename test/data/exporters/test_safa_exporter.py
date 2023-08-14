import os
from typing import List

from tgen.common.util.json_util import JsonUtil
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

    def test_smoke_test(self):
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
        """
        Tests the ability to export generated links with explanations.
        """
        source = "S1"
        target = "T2"
        score = 0.4
        explanation = "EXPLANATION"
        source_type = "source"
        target_type = "target"
        trace_file_name = f"{source_type}2{target_type}.json"

        artifact_layers = {
            source_type: {f"S{i}": "dummy text" for i in range(3)},
            target_type: {f"T{i}": "dummy text" for i in range(3)}
        }
        layers: List[TraceLayer] = [TraceLayer(child=source_type, parent=target_type)]
        true_links: List[TracePredictionEntry] = [{
            "source": source,
            "target": target,
            "score": score,
            "explanation": explanation
        }]
        api_definition = ApiDefinition(artifact_layers=artifact_layers, layers=layers, true_links=true_links)
        api_project_reader = ApiProjectReader(api_definition=api_definition)
        trace_dataset_creator = TraceDatasetCreator(project_reader=api_project_reader)
        safa_exporter = SafaExporter(TEST_OUTPUT_DIR, dataset_creator=trace_dataset_creator)
        safa_exporter.export()

        trace_file_path = os.path.join(TEST_OUTPUT_DIR, trace_file_name)
        trace_file = JsonUtil.read_json_file(trace_file_path)
        traces = trace_file["traces"]

        self.assertEqual(1, len(traces))
        trace = traces[0]
        self.assertEqual(trace["sourceName"], "S1")
        self.assertEqual(trace["targetName"], "T2")
        self.assertEqual(trace["score"], score)
        self.assertEqual(trace["explanation"], explanation)
        self.assertEqual(trace["approvalStatus"], "UNREVIEWED")
        self.assertEqual(trace["traceType"], "GENERATED")

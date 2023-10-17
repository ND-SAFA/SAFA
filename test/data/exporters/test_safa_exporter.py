import os
from typing import List

import pandas as pd

from tgen.common.objects.artifact import Artifact
from tgen.common.util.file_util import FileUtil
from tgen.common.util.json_util import JsonUtil
from tgen.common.objects.trace import Trace
from tgen.data.creators.trace_dataset_creator import TraceDatasetCreator
from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame
from tgen.data.keys.structure_keys import ArtifactKeys
from tgen.data.exporters.safa_exporter import SafaExporter
from tgen.data.readers.api_project_reader import ApiProjectReader
from tgen.data.readers.definitions.api_definition import ApiDefinition
from tgen.data.readers.structured_project_reader import StructuredProjectReader
from tgen.testres.base_tests.base_test import BaseTest
from tgen.testres.object_creator import ObjectCreator
from tgen.testres.paths.paths import TEST_OUTPUT_DIR
from tgen.common.objects.trace_layer import TraceLayer


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
        source_type = "source_type"
        target_type = "target_type"
        trace_file_name = f"{source_type}2{target_type}.json"

        source_artifacts = [Artifact(id=f"S{i}", content="dummy text", layer_id=source_type) for i in range(3)]
        target_artifacts = [Artifact(id=f"T{i}", content="dummy text", layer_id=target_type) for i in range(3)]

        artifacts = source_artifacts + target_artifacts
        layers: List[TraceLayer] = [TraceLayer(child=source_type, parent=target_type)]
        links: List[Trace] = [Trace(source=source, target=target, score=score, explanation=explanation)]
        api_definition = ApiDefinition(artifacts=artifacts, layers=layers, links=links)
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

    def test_summaries(self):
        """
        Tests that summaries are included in the safa export.
        """
        artifact_id = "RE1"
        artifact_content = "This is a body"
        artifact_type = "source"
        artifact_summary = "This is a summary"
        artifact_type_file_name = f"{artifact_type}.csv"

        artifact_export_path = os.path.join(TEST_OUTPUT_DIR, "source.csv")
        entries = [{"id": artifact_id, "content": artifact_content, "layer_id": artifact_type, "summary": artifact_summary}]
        artifact_df = ArtifactDataFrame(entries)
        artifact_df.to_csv(artifact_export_path)
        tim_json = {"artifacts": [{
            "fileName": artifact_type_file_name,
            "type": artifact_type
        }], "traces": []}
        FileUtil.write(tim_json, os.path.join(TEST_OUTPUT_DIR, "tim.json"))

        export_dir = os.path.join(TEST_OUTPUT_DIR, "export")
        project_reader = StructuredProjectReader(project_path=TEST_OUTPUT_DIR)
        trace_dataset_creator = TraceDatasetCreator(project_reader=project_reader)
        safa_exporter = SafaExporter(export_dir, trace_dataset_creator)
        safa_exporter.export()

        artifact_exported_df = pd.read_csv(os.path.join(export_dir, artifact_type_file_name))
        self.assertEqual(1, len(artifact_exported_df))
        artifact = artifact_exported_df.iloc[0]
        self.assertEqual(artifact_id, artifact[ArtifactKeys.ID.value])
        self.assertEqual(artifact_content, artifact[ArtifactKeys.CONTENT.value])
        self.assertEqual(artifact_summary, artifact[ArtifactKeys.SUMMARY.value])

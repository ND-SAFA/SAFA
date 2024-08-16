import os

from gen_common.data.creators.prompt_dataset_creator import PromptDatasetCreator
from gen_common.data.creators.trace_dataset_creator import TraceDatasetCreator
from gen_common.data.exporters.api_exporter import ApiExporter
from gen_common.data.exporters.csv_exporter import CSVExporter
from gen_common.data.exporters.dataframe_exporter import DataFrameExporter
from gen_common.data.exporters.prompt_dataset_exporter import PromptDatasetExporter
from gen_common.data.exporters.safa_exporter import SafaExporter
from gen_common.data.readers.api_project_reader import ApiProjectReader
from gen_common.data.readers.artifact_project_reader import ArtifactProjectReader
from gen_common.data.readers.csv_project_reader import CsvProjectReader
from gen_common.data.readers.dataframe_project_reader import DataFrameProjectReader
from gen_common.data.readers.prompt_project_reader import PromptProjectReader
from gen_common.data.readers.structured_project_reader import StructuredProjectReader
from gen_common.data.summarizer.summary import Summary
from gen_common.util import EnumDict
from gen_common_test.base_tests.base_test import BaseTest
from gen_common_test.paths.base_paths import TEST_OUTPUT_DIR
from gen_common_test.testprojects.prompt_test_project import PromptTestProject


class TestPromptDatasetExporter(BaseTest):

    def test_export_trace_dataset(self):
        trace_dataset_creator = PromptTestProject.get_trace_dataset_creator()
        dataset_creator_orig = PromptDatasetCreator(trace_dataset_creator=trace_dataset_creator)
        dataset_exporter_to_reader = {DataFrameExporter: DataFrameProjectReader,
                                      SafaExporter: StructuredProjectReader,
                                      CSVExporter: CsvProjectReader,
                                      ApiExporter: ApiProjectReader
                                      }

        i = 0
        for dataset_exporter, project_reader in dataset_exporter_to_reader.items():
            export_path = os.path.join(TEST_OUTPUT_DIR, f"prompt_dataset_{i}")
            if issubclass(dataset_exporter, CSVExporter):
                export_path = os.path.join(export_path, "dataset.csv")
            elif issubclass(dataset_exporter, ApiExporter):
                export_path = os.path.join(export_path, "dataset.json")
            dataset = dataset_creator_orig.create()
            dataset.project_summary = Summary(overview=EnumDict({"chunks": ["summary of project"],
                                                                 "title": "overview"}))
            PromptDatasetExporter(export_path, dataset_exporter, dataset=dataset).export()
            trace_dataset_creator = TraceDatasetCreator(project_reader=project_reader(project_path=export_path))
            new_dataset = PromptDatasetCreator(trace_dataset_creator=trace_dataset_creator).create()
            PromptTestProject.verify_dataset(self, new_dataset)
            self.assertEqual(dataset.project_summary, new_dataset.project_summary)
            i += 1

    def test_export_df(self):
        artifact_reader = PromptTestProject.get_artifact_project_reader()
        prompt_reader = PromptTestProject.get_project_reader()
        readers = [artifact_reader, prompt_reader]

        i = 0
        for reader in readers:
            dataset_creator_orig = PromptDatasetCreator(project_reader=reader)
            dataset = dataset_creator_orig.create()
            export_path = os.path.join(TEST_OUTPUT_DIR, f"prompt_dataset_{i}")
            if isinstance(reader, PromptProjectReader):
                export_path = os.path.join(export_path, "dataset.jsonl")
            PromptDatasetExporter(export_path, dataset=dataset).export()
            new_dataset = PromptDatasetCreator(
                project_reader=reader.__class__(project_path=export_path))
            if isinstance(reader, ArtifactProjectReader):
                new_dataset = new_dataset.create()
            PromptTestProject.verify_dataset(self, new_dataset)
            i += 1

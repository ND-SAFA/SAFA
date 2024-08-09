from common_resources.data.creators.prompt_dataset_creator import PromptDatasetCreator
from common_resources.data.creators.serialized_dataset_creator import SerializedDatasetCreator
from common_resources.data.exporters.serializable_exporter import SerializableExporter
from common_resources.data.summarizer.summary import Summary, SummarySection
from common_resources.tools.util.enum_util import EnumDict
from common_resources_test.base_tests.base_test import BaseTest
from common_resources_test.testprojects.prompt_test_project import PromptTestProject


class TestSerializableDatasetExporter(BaseTest):

    def test_export_trace_dataset(self):
        trace_dataset_creator = PromptTestProject.get_trace_dataset_creator()
        dataset_creator_orig = PromptDatasetCreator(trace_dataset_creator=trace_dataset_creator,
                                                    project_summary=Summary(overview=EnumDict({"title": "overview",
                                                                                               "chunks": ["summary of project"]})))

        dataset = dataset_creator_orig.create()
        serializable_dataset = SerializableExporter(dataset=dataset).export()
        new_dataset = SerializedDatasetCreator(serialized_dataset=serializable_dataset).create()
        PromptTestProject.verify_dataset(self, new_dataset)
        self.assertDictEqual(dataset.project_summary, new_dataset.project_summary)

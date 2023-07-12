from tgen.data.creators.multi_trace_dataset_creator import MultiTraceDatasetCreator
from tgen.data.creators.trace_dataset_creator import TraceDatasetCreator
from tgen.testres.base_tests.base_trace_test import BaseTraceTest
from tgen.testres.definition_creator import DefinitionCreator
from tgen.testres.paths.project_paths import CSV_PROJECT_PATH, STRUCTURE_PROJECT_PATH
from tgen.testres.testprojects.csv_test_project import CsvTestProject
from tgen.testres.testprojects.structured_test_project import StructuredTestProject
from tgen.variables.typed_definition_variable import TypedDefinitionVariable


class TestMultiTraceDatasetCreator(BaseTraceTest):

    def test_create(self):
        """
        Tests that creating multi-dataset contains the datasets within it.
        """
        multi_dataset_creator = self.get_multi_trace_dataset_creator()
        multi_dataset = multi_dataset_creator.create()
        expected_projects = [StructuredTestProject(), CsvTestProject()]
        expected_datasets = [TraceDatasetCreator(project.get_project_reader()).create() for project in expected_projects]
        for dataset in expected_datasets:
            for link_id in dataset.trace_df.index:
                self.assertIn(link_id, multi_dataset.trace_df)
            for link_id in dataset._pos_link_ids:
                self.assertIn(link_id, multi_dataset._pos_link_ids)
            for link_id in dataset._neg_link_ids:
                self.assertIn(link_id, multi_dataset._neg_link_ids)

    @staticmethod
    def get_multi_trace_dataset_creator():
        dataset_creator_definition_multi = {
            "project_readers": [{
                TypedDefinitionVariable.OBJECT_TYPE_KEY: "STRUCTURE",
                "project_path": STRUCTURE_PROJECT_PATH
            }, {
                TypedDefinitionVariable.OBJECT_TYPE_KEY: "CSV",
                "project_path": CSV_PROJECT_PATH,
                "overrides": {
                    "allowed_orphans": 2
                }
            }]
        }
        return DefinitionCreator.create(MultiTraceDatasetCreator, dataset_creator_definition_multi)

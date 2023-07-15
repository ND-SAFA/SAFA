import os
from typing import List

from tgen.data.creators.trace_dataset_creator import TraceDatasetCreator
from tgen.data.exporters.api_exporter import ApiExporter
from tgen.data.readers.api_project_reader import ApiProjectReader
from tgen.testres.base_tests.base_test import BaseTest
from tgen.testres.paths.paths import TEST_OUTPUT_DIR
from tgen.testres.test_assertions import TestAssertions
from tgen.testres.testprojects.api_test_project import ApiTestProject
from tgen.util.json_util import JsonUtil


class TestApiExporter(BaseTest):

    def test_export(self):
        export_path = os.path.join(TEST_OUTPUT_DIR, "api.json")
        orig_creator = TraceDatasetCreator(ApiTestProject.get_project_reader(), allowed_missing_sources=100,
                                           allowed_missing_targets=100, allowed_orphans=100)
        orig_dataset = orig_creator.create()
        exporter = ApiExporter(dataset_creator=orig_creator, export_path=export_path)
        api_definition = exporter.export()
        exported_api_definition_dict = JsonUtil.read_json_file(export_path)
        exported_api_definition_dict["true_links"] = [link for link in exported_api_definition_dict["true_links"]]
        api_definition_dict = api_definition.as_dict()
        self.assertDictEqual(exported_api_definition_dict, api_definition_dict)
        exported_dataset = TraceDatasetCreator(ApiProjectReader(api_definition), allowed_missing_sources=100,
                                               allowed_missing_targets=100, allowed_orphans=100).create()
        TestAssertions.verify_entities_in_df(self, self.df_as_queries(orig_dataset.artifact_df), exported_dataset.artifact_df)
        TestAssertions.verify_entities_in_df(self, self.df_as_queries(orig_dataset.trace_df), exported_dataset.trace_df)
        TestAssertions.verify_entities_in_df(self, self.df_as_queries(orig_dataset.layer_df), exported_dataset.layer_df)

    @staticmethod
    def df_as_queries(df) -> List[dict]:
        return [query for _, query in df.itertuples()]

import os
from typing import List

from gen_common.data.creators.trace_dataset_creator import TraceDatasetCreator
from gen_common.data.exporters.api_exporter import ApiExporter
from gen_common.data.readers.api_project_reader import ApiProjectReader
from gen_common.util.dict_util import DictUtil
from gen_common.util.json_util import JsonUtil
from gen_common_test.base.tests.base_test import BaseTest
from gen_common_test.paths.base_paths import TEST_OUTPUT_DIR
from gen_common_test.testprojects.api_test_project import ApiTestProject


class TestApiExporter(BaseTest):

    def test_export(self):
        export_path = os.path.join(TEST_OUTPUT_DIR, "api.json")
        orig_creator = TraceDatasetCreator(ApiTestProject.get_project_reader(), allowed_missing_sources=100,
                                           allowed_missing_targets=100, allowed_orphans=100)
        orig_dataset = orig_creator.create()
        exporter = ApiExporter(dataset_creator=orig_creator, export_path=export_path)
        api_definition = exporter.export()
        exported_api_definition_dict = JsonUtil.read_json_file(export_path)
        api_definition_dict = JsonUtil.as_dict(api_definition)
        api_definition_dict = DictUtil.convert_iterables_to_lists(api_definition_dict)
        self.assertListEqual(exported_api_definition_dict["links"], api_definition_dict["links"])
        self.assertListEqual(exported_api_definition_dict["layers"], api_definition_dict["layers"])
        self.assertListEqual(exported_api_definition_dict["artifacts"], api_definition_dict["artifacts"])
        exported_dataset = TraceDatasetCreator(ApiProjectReader(api_definition), allowed_missing_sources=100,
                                               allowed_missing_targets=100, allowed_orphans=100).create()
        self.verify_entities_in_df(self.df_as_queries(orig_dataset.artifact_df), exported_dataset.artifact_df)
        self.verify_entities_in_df(self.df_as_queries(orig_dataset.trace_df), exported_dataset.trace_df)
        self.verify_entities_in_df(self.df_as_queries(orig_dataset.layer_df), exported_dataset.layer_df)

    @staticmethod
    def df_as_queries(df) -> List[dict]:
        return [query for _, query in df.itertuples()]

from data.datasets.creators.classic_trace_dataset_creator import ClassicTraceDatasetCreator
from test.base_trace_test import BaseTraceTest
from test.test_assertions import TestAssertions
from test.test_data_manager import TestDataManager
from util.object_creator import ObjectCreator


class TestClassicTraceDatasetCreator(BaseTraceTest):

    def test_create(self):
        dataset_creator = self.get_classic_trace_dataset_creator()
        dataset = dataset_creator.create()
        TestDataManager.get_positive_links()
        TestAssertions.assert_lists_have_the_same_vals(self, dataset.pos_link_ids,
                                                       TestDataManager.get_positive_link_ids())
        TestAssertions.assert_lists_have_the_same_vals(self, dataset.links, TestDataManager.get_all_link_ids())
        TestAssertions.assert_lists_have_the_same_vals(self, dataset.neg_link_ids,
                                                       TestDataManager.get_negative_link_ids())

    def test_generate_all_links(self):
        dataset_creator = self.get_classic_trace_dataset_creator()
        TestDataManager.get_positive_links()
        links = dataset_creator._generate_all_links(
            self.get_source_layer(),
            self.get_target_layer(),
            set(TestDataManager.get_positive_link_ids()))
        resulting_links = [(link.source.id, link.target.id) for link in links.values()]
        TestAssertions.assert_lists_have_the_same_vals(self,
                                                       resulting_links,
                                                       TestDataManager.get_all_links())

    def test_make_artifacts(self):
        dataset_creator = self.get_classic_trace_dataset_creator()
        artifacts = dataset_creator._make_artifacts(self.get_source_layer()[0])
        TestAssertions.assert_lists_have_the_same_vals(self, self.get_source_layer()[0].keys(),
                                                       [artifact.id for artifact in artifacts])

    def test_get_pos_link_ids(self):
        dataset_creator = self.get_classic_trace_dataset_creator()
        pos_link_ids = dataset_creator._get_pos_link_ids(TestDataManager.get_positive_links())
        TestAssertions.assert_lists_have_the_same_vals(self, pos_link_ids, TestDataManager.get_positive_link_ids())

    def test_create_links_for_layer(self):
        dataset_creator = self.get_classic_trace_dataset_creator()
        pos_link_ids = dataset_creator._get_pos_link_ids(TestDataManager.get_positive_links())
        links = dataset_creator._create_links_for_layer(
            TestDataManager._create_test_artifact(self.get_source_layer()[0]),
            TestDataManager._create_test_artifact(self.get_target_layer()[0]),
            pos_link_ids)
        self.assertEquals(len(links), len(self.get_source_layer()[0]) * len(self.get_target_layer()[0]))

    def test_create_links_for_layer_linked_targets_only(self):
        dataset_creator = self.get_classic_trace_dataset_creator(use_linked_targets_only=True)
        pos_link_ids = dataset_creator._get_pos_link_ids(TestDataManager.get_positive_links())
        links = dataset_creator._create_links_for_layer(
            TestDataManager._create_test_artifact(self.get_source_layer()[0]),
            TestDataManager._create_test_artifact(self.get_target_layer()[0]),
            pos_link_ids)
        for link in links.values():
            self.assertIn(link.target.id, TestDataManager.get_linked_targets())

    def get_source_layer(self):
        return self.get_artifact_layer(TestDataManager.Keys.SOURCE)

    def get_target_layer(self):
        return self.get_artifact_layer(TestDataManager.Keys.TARGET)

    def get_artifact_layer(self, key: str):
        return TestDataManager.get_path([TestDataManager.Keys.ARTIFACTS, key])

    def get_classic_trace_dataset_creator(self, **kwargs):
        return ObjectCreator.create(ClassicTraceDatasetCreator, **kwargs)

from test.base_test import BaseTest
from tracer.dataset.creators.classic_trace_dataset_creator import ClassicTraceDatasetCreator


class TestClassicTraceDatasetCreator(BaseTest):

    def test_get_pos_link_ids(self):
        dataset_creator = self.get_classic_trace_dataset_creator()
        pos_link_ids = dataset_creator._get_pos_link_ids(self.POS_LINKS)
        expected_pos_link_ids = list(self.get_links(self.POS_LINKS).keys())
        self.assert_lists_have_the_same_vals(pos_link_ids, expected_pos_link_ids)

    def test_create_links_for_layer(self):
        dataset_creator = self.get_classic_trace_dataset_creator()
        pos_link_ids = dataset_creator._get_pos_link_ids(self.POS_LINKS)
        links = dataset_creator._create_links_for_layer(self.get_test_artifacts(self.SOURCE_LAYERS[0]),
                                                        self.get_test_artifacts(self.TARGET_LAYERS[0]),
                                                        pos_link_ids)
        self.assert_lists_have_the_same_vals([(link.source.id, link.target.id) for link in links.values()], self.ALL_TEST_LINKS)

    def get_classic_trace_dataset_creator(self, use_linked_targets_only: bool = False):
        return ClassicTraceDatasetCreator(source_layers=self.SOURCE_LAYERS, target_layers=self.TARGET_LAYERS,
                                          true_links=self.POS_LINKS, pre_processing_params=self.PRE_PROCESSING_PARAMS,
                                          use_linked_targets_only=False)

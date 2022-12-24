from data.datasets.creators.classic_trace_dataset_creator import ClassicTraceDatasetCreator
from test.base_trace_test import BaseTraceTest


class TestClassicTraceDatasetCreator(BaseTraceTest):

    def test_create(self):
        dataset_creator = self.get_classic_trace_dataset_creator()
        dataset = dataset_creator.create()
        self.assert_lists_have_the_same_vals(dataset.pos_link_ids, self.get_link_ids(self.POS_LINKS))
        self.assert_lists_have_the_same_vals(dataset.links, self.get_link_ids(self.ALL_TEST_LINKS))
        self.assert_lists_have_the_same_vals(dataset.neg_link_ids, self.get_link_ids(self.NEG_LINKS))

    def test_generate_all_links(self):
        dataset_creator = self.get_classic_trace_dataset_creator()
        pos_link_ids = dataset_creator._get_pos_link_ids(self.POS_LINKS)
        links = dataset_creator._generate_all_links(self.SOURCE_LAYERS, self.TARGET_LAYERS,
                                                    pos_link_ids)
        self.assert_lists_have_the_same_vals([(link.source.id, link.target.id) for link in links.values()],
                                             self.ALL_TEST_LINKS)

    def test_make_artifacts(self):
        dataset_creator = self.get_classic_trace_dataset_creator()
        artifacts = dataset_creator._make_artifacts(self.SOURCE_LAYERS[0])
        self.assert_lists_have_the_same_vals(self.SOURCE_LAYERS[0].keys(), [artifact.id for artifact in artifacts])

    def test_get_pos_link_ids(self):
        dataset_creator = self.get_classic_trace_dataset_creator()
        pos_link_ids = dataset_creator._get_pos_link_ids(self.POS_LINKS)
        self.assert_lists_have_the_same_vals(pos_link_ids, self.get_link_ids(self.POS_LINKS))

    def test_create_links_for_layer(self):
        dataset_creator = self.get_classic_trace_dataset_creator()
        pos_link_ids = dataset_creator._get_pos_link_ids(self.POS_LINKS)
        links = dataset_creator._create_links_for_layer(self.get_test_artifacts(self.SOURCE_LAYERS[0]),
                                                        self.get_test_artifacts(self.TARGET_LAYERS[0]),
                                                        pos_link_ids)
        self.assertEquals(len(links), len(self.SOURCE_LAYERS[0]) * len(self.TARGET_LAYERS[0]))

    def test_create_links_for_layer_linked_targets_only(self):
        dataset_creator = self.get_classic_trace_dataset_creator(use_linked_targets_only=True)
        pos_link_ids = dataset_creator._get_pos_link_ids(self.POS_LINKS)
        links = dataset_creator._create_links_for_layer(self.get_test_artifacts(self.SOURCE_LAYERS[0]),
                                                        self.get_test_artifacts(self.TARGET_LAYERS[0]),
                                                        pos_link_ids)
        for link in links.values():
            self.assertIn(link.target.id, self.LINKED_TARGETS)

    def get_classic_trace_dataset_creator(self, use_linked_targets_only: bool = False):
        return ClassicTraceDatasetCreator(source_layers=self.SOURCE_LAYERS, target_layers=self.TARGET_LAYERS,
                                          true_links=self.POS_LINKS, data_cleaner=self.DATA_CLEANER,
                                          use_linked_targets_only=use_linked_targets_only)

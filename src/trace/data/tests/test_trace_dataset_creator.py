from django.test import TestCase

from common.models.model_generator import ModelGenerator
from trace.data.artifact import Artifact
from trace.data.trace_dataset_creator import TraceDatasetCreator
from mock import patch
import mock
from trace.data.trace_link import TraceLink


def fake_extract_feature_info(feature, prefix=''):
    return {prefix + "feature_info": feature}


class TestTraceDatasetCreator(TestCase):
    TEST_S_ARTS = {"s1": "token1",
                   "s2": "token2",
                   "s3": "token3"}

    TEST_T_ARTS = {"t1": "token1",
                   "t2": "token2",
                   "t3": "token3"}

    TEST_POS_LINKS = [("s1", "t1"), ("s2", "t1"), ("s3", "t2")]
    ALL_LINKS = [("s1", "t1"), ("s2", "t1"), ("s3", "t1"),
                 ("s1", "t2"), ("s2", "t2"), ("s3", "t2"),
                 ("s1", "t3"), ("s2", "t3"), ("s3", "t3")]
    LINKED_TARGETS = ["t1", "t2"]
    UNLINKED_TARGET = "t3"

    TEST_FEATURE = {"irrelevant_key1": "k",
                    "input_ids": "a",
                    "token_type_ids": "l",
                    "attention_mask": 4,
                    "irrelevant_key2": "evr"}
    VAlIDATION_PERCENTAGE = 0.3
    EXPECTED_VALIDATION_SIZE = 3
    EXPECTED_FEATURE_KEYS = ["input_ids", "token_type_ids", "attention_mask"]
    IRRELEVANT_FEATURE_KEYS = ["irrelevant_key1", "irrelevant_key2"]
    TEST_MODEL_GENERATOR = ModelGenerator("bert_trace_single", "path")

    @patch.object(TraceDatasetCreator, "_get_feature_entry")
    def test_get_training_and_validation_dataset(self, get_feature_entry_mock: mock.MagicMock):
        get_feature_entry_mock.side_effect = fake_extract_feature_info
        test_trace_dataset_creator = self.get_test_trace_dataset_creator()
        training_dataset = test_trace_dataset_creator.get_training_dataset()
        validation_dataset = test_trace_dataset_creator.get_validation_dataset()

        training_link_ids = self.get_dataset_link_attrs(training_dataset)
        validation_link_ids = self.get_dataset_link_attrs(validation_dataset)
        for link_id in validation_link_ids:
            self.assertNotIn(link_id, training_link_ids)

    @patch.object(TraceDatasetCreator, "_get_feature_entry")
    def test_get_training_dataset(self, get_feature_entry_mock: mock.MagicMock):
        get_feature_entry_mock.side_effect = fake_extract_feature_info
        resample_rate = 3
        expected_dataset_size = self.get_expected_train_dataset_size(resample_rate)

        test_trace_dataset_creator = self.get_test_trace_dataset_creator()
        training_dataset = test_trace_dataset_creator.get_training_dataset(resample_rate)
        self.assertEquals(len(get_feature_entry_mock.mock_calls), len(self.ALL_LINKS) - self.EXPECTED_VALIDATION_SIZE)
        self.assertEquals(len(training_dataset), expected_dataset_size)

        pos_links = self.get_links(self.TEST_POS_LINKS)
        train_dataset_links = self.get_dataset_link_attrs(training_dataset)
        pos_link_count = 0
        for link_id in train_dataset_links:
            if link_id in pos_links:
                pos_link_count += 1
        self.assertEquals(pos_link_count, expected_dataset_size / 2)

        # should not call get_feature_entries second time
        get_feature_entry_mock.called = False
        test_trace_dataset_creator.get_training_dataset()
        self.assertFalse(get_feature_entry_mock.called)

    @patch.object(TraceDatasetCreator, "_get_feature_entry")
    def test_get_validation_dataset_full(self, get_feature_entry_mock: mock.MagicMock):
        get_feature_entry_mock.side_effect = fake_extract_feature_info
        test_trace_dataset_creator = self.get_test_trace_dataset_creator()
        validation_dataset = test_trace_dataset_creator.get_validation_dataset()
        self.assertEquals(len(get_feature_entry_mock.mock_calls), self.EXPECTED_VALIDATION_SIZE)
        self.assertEquals(len(validation_dataset), self.EXPECTED_VALIDATION_SIZE)

        # should not call get_feature_entries second time
        get_feature_entry_mock.called = False
        test_trace_dataset_creator.get_validation_dataset()
        self.assertFalse(get_feature_entry_mock.called)

    @patch.object(TraceDatasetCreator, "_get_feature_entry")
    def test_get_validation_dataset_small(self, get_feature_entry_mock: mock.MagicMock):
        get_feature_entry_mock.side_effect = fake_extract_feature_info
        dataset_size = 2
        test_trace_dataset_creator = self.get_test_trace_dataset_creator()
        validation_dataset = test_trace_dataset_creator.get_validation_dataset(dataset_size=dataset_size)
        self.assertEquals(len(get_feature_entry_mock.mock_calls), dataset_size)
        self.assertEquals(len(validation_dataset), dataset_size)

    @patch.object(TraceDatasetCreator, "_get_feature_entry")
    def test_get_validation_dataset_linked_targets_only(self, get_feature_entry_mock: mock.MagicMock):
        get_feature_entry_mock.side_effect = fake_extract_feature_info
        test_trace_dataset_creator = self.get_test_trace_dataset_creator()
        validation_dataset = test_trace_dataset_creator.get_validation_dataset(linked_targets_only=True)

        self.assertLessEqual(len(get_feature_entry_mock.mock_calls), self.EXPECTED_VALIDATION_SIZE)
        self.assertLessEqual(len(validation_dataset), self.EXPECTED_VALIDATION_SIZE)

        validation_dataset_targets = self.get_dataset_link_attrs(validation_dataset, attr="target")
        for target in validation_dataset_targets:
            self.assertNotEquals(target.id_, self.UNLINKED_TARGET)

    @patch.object(TraceDatasetCreator, "_get_feature_entry")
    def test_get_prediction_dataset(self, get_feature_entry_mock: mock.MagicMock):
        get_feature_entry_mock.side_effect = fake_extract_feature_info
        test_trace_dataset_creator = self.get_test_trace_dataset_creator(include_links=False)
        prediction_dataset = test_trace_dataset_creator.get_prediction_dataset()
        self.assertEquals(len(get_feature_entry_mock.mock_calls), len(self.ALL_LINKS))

        self.assertEqual(len(prediction_dataset), len(self.ALL_LINKS))
        all_links = self.get_links(self.ALL_LINKS)

        prediction_dataset_links = self.get_dataset_link_attrs(prediction_dataset)
        for link in all_links.keys():
            self.assertIn(link, prediction_dataset_links)

        # should not call get_feature_entries second time
        get_feature_entry_mock.called = False
        test_trace_dataset_creator.get_prediction_dataset()
        self.assertFalse(get_feature_entry_mock.called)

    # TODO
    def test_update_embeddings(self):
        pass

    # TODO
    def test_update_artifact_embedding(self):
        pass

    @patch.object(TraceDatasetCreator, "_extract_feature_info")
    def test_get_feature_entry_siamese(self, extract_feature_info_mock: mock.MagicMock):
        extract_feature_info_mock.side_effect = fake_extract_feature_info

        test_trace_dataset_creator = self.get_test_trace_dataset_creator(model_generator=ModelGenerator("bert_trace_siamese", "path"))
        source, target = self.TEST_POS_LINKS[0]
        test_link = self.get_test_link(source, target)
        feature_entry = test_trace_dataset_creator._get_feature_entry(test_link)

        self.feature_entry_test(feature_entry, test_link)
        self.assertEquals(extract_feature_info_mock.call_count, 2)
        extract_feature_info_mock.assert_any_call(test_link.source.token, "s_")
        extract_feature_info_mock.assert_any_call(test_link.target.token, "t_")

    @patch.object(TraceDatasetCreator, "_extract_feature_info")
    def test_get_feature_entry_single(self, extract_feature_info_mock: mock.MagicMock):
        extract_feature_info_mock.side_effect = fake_extract_feature_info

        test_trace_dataset_creator = self.get_test_trace_dataset_creator()
        source, target = self.TEST_POS_LINKS[0]
        test_link = self.get_test_link(source, target)
        feature_entry = test_trace_dataset_creator._get_feature_entry(test_link)

        self.feature_entry_test(feature_entry, test_link)
        self.assertEquals(extract_feature_info_mock.call_count, 1)

    @patch.object(TraceDatasetCreator, '_get_feature_entry')
    def test_get_feature_entries(self, get_feature_entry_mock: mock.MagicMock):
        get_feature_entry_mock.return_value = {"feature_entry": "value"}

        test_trace_dataset_creator = self.get_test_trace_dataset_creator()
        link_ids = self.get_links(self.TEST_POS_LINKS).keys()
        feature_entries = test_trace_dataset_creator._get_feature_entries(link_ids, 5)

        self.assertEquals(len(feature_entries), 5 * len(self.TEST_POS_LINKS))
        self.assertEquals(get_feature_entry_mock.call_count, len(self.TEST_POS_LINKS))

    def test_get_data_split(self):
        test_trace_dataset_creator = self.get_test_trace_dataset_creator()
        test_split = test_trace_dataset_creator._get_data_split(self.ALL_LINKS)
        val_split = test_trace_dataset_creator._get_data_split(self.ALL_LINKS, for_validation=True)

        self.assertEquals(len(test_split), len(self.ALL_LINKS) - self.EXPECTED_VALIDATION_SIZE)
        self.assertEquals(len(val_split), self.EXPECTED_VALIDATION_SIZE)

        for link in val_split:
            self.assertNotIn(link, test_split)

    def test_get_train_split_size(self):
        test_trace_dataset_creator = self.get_test_trace_dataset_creator()
        split_size = test_trace_dataset_creator._get_train_split_size(self.ALL_LINKS)
        self.assertEquals(split_size, len(self.ALL_LINKS) - self.EXPECTED_VALIDATION_SIZE)

    def test_reduce_to_linked_targets_only(self):
        test_trace_dataset_creator = self.get_test_trace_dataset_creator()
        orig_links = self.get_links(self.ALL_LINKS)
        expected_links = self.get_links(self.ALL_LINKS[:6])  # exclude links with t3

        linked_targets_only = test_trace_dataset_creator._reduce_to_linked_targets_only(orig_links.keys())

        self.assertEquals(len(linked_targets_only), len(expected_links))
        for link_id in linked_targets_only:
            self.assertIn(link_id, expected_links)

    @patch.object(TraceDatasetCreator, '_create_pos_and_neg_links')
    def test_create_links_with_no_true_links(self, create_pos_and_neg_links_mock: mock.MagicMock):
        links, pos_link_ids, neg_link_ids = TraceDatasetCreator._create_links(self.TEST_MODEL_GENERATOR, self.TEST_S_ARTS,
                                                                              self.TEST_T_ARTS)
        self.links_test(links)
        self.assertFalse(create_pos_and_neg_links_mock.called)

    @patch.object(TraceDatasetCreator, '_create_pos_and_neg_links')
    def test_create_links_with_true_links(self, create_pos_and_neg_links_mock: mock.MagicMock):
        create_pos_and_neg_links_mock.return_value = ([1, 2, 3], [4, 5, 6])
        links, pos_link_ids, neg_link_ids = TraceDatasetCreator._create_links(self.TEST_MODEL_GENERATOR, self.TEST_S_ARTS,
                                                                              self.TEST_T_ARTS, self.TEST_POS_LINKS)
        self.links_test(links)
        self.assertTrue(create_pos_and_neg_links_mock.called)

    def test_create_pos_and_neg_links(self):
        all_links = self.get_links(self.ALL_LINKS)
        pos_link_ids, neg_link_ids = TraceDatasetCreator._create_pos_and_neg_links(self.TEST_POS_LINKS, all_links)

        self.assertEquals(len(pos_link_ids), len(self.TEST_POS_LINKS))
        self.assertEquals(len(neg_link_ids), len(self.ALL_LINKS) - len(self.TEST_POS_LINKS))

        for link in self.TEST_POS_LINKS:
            id_ = TraceLink.generate_link_id(link[0], link[1])
            self.assertIn(id_, pos_link_ids)

        for link in self.ALL_LINKS:
            id_ = TraceLink.generate_link_id(link[0], link[1])
            if id_ in pos_link_ids:
                self.assertNotIn(id_, neg_link_ids)
                self.assertTrue(all_links[id_].is_true_link)
            else:
                self.assertIn(id_, neg_link_ids)
                self.assertFalse(all_links[id_].is_true_link)

    def test_extract_feature_info_no_prefix(self):
        feature_info = TraceDatasetCreator._extract_feature_info(self.TEST_FEATURE)

        for key in self.EXPECTED_FEATURE_KEYS:
            self.assertIn(key, feature_info)
            self.assertEquals(feature_info[key], self.TEST_FEATURE[key])
        for key in self.IRRELEVANT_FEATURE_KEYS:
            self.assertNotIn(key, feature_info)

    def test_extract_feature_info_with_prefix(self):
        prefix = "s_"
        feature_info = TraceDatasetCreator._extract_feature_info(self.TEST_FEATURE, prefix)

        for key in self.EXPECTED_FEATURE_KEYS:
            self.assertIn(prefix + key, feature_info)
            self.assertEquals(feature_info[prefix + key], self.TEST_FEATURE[key])
        for key in self.IRRELEVANT_FEATURE_KEYS:
            self.assertNotIn(prefix + key, feature_info)

    def test_change_data_size_bigger(self):
        new_dataset = TraceDatasetCreator._change_data_size(self.TEST_POS_LINKS, 5)
        self.assertEquals(len(new_dataset), 5)

    def test_change_data_size_duplicates(self):
        new_dataset = TraceDatasetCreator._change_data_size(self.TEST_POS_LINKS, 2, True)
        self.assertEquals(len(new_dataset), 2)

    def test_reduce_data_size_smaller_no_duplicates(self):
        new_dataset = TraceDatasetCreator._change_data_size(self.TEST_POS_LINKS, 2, False)
        self.assertEquals(len(set(new_dataset)), 2)

    def tests_get_linked_targets_only(self):
        linked_targets = TraceDatasetCreator._get_linked_targets_only(self.TEST_POS_LINKS)

        for target in self.LINKED_TARGETS:
            self.assertIn(target, linked_targets)

        self.assertNotIn(self.UNLINKED_TARGET, linked_targets)

    # ============= HELPER METHODS =============
    def get_dataset_link_attrs(self, dataset, attr="id_"):
        return [getattr(feature_entry["feature_info"], attr) for feature_entry in dataset]

    def feature_entry_test(self, feature_entry, test_link):
        self.assertIn("sid", feature_entry)
        self.assertEquals(feature_entry["sid"], test_link.source.id_)

        self.assertIn("tid", feature_entry)
        self.assertEquals(feature_entry["tid"], test_link.target.id_)

        self.assertIn("label", feature_entry)
        self.assertEquals(feature_entry["label"], 0)

    def links_test(self, links):
        self.assertEquals(len(links), len(self.ALL_LINKS))
        for link in self.ALL_LINKS:
            id_ = TraceLink.generate_link_id(link[0], link[1])
            self.assertIn(id_, links)
            self.assertEquals(link[0], links[id_].source.id_)
            self.assertEquals(link[1], links[id_].target.id_)

    def get_links(self, link_list):
        links = {}
        for source, target in link_list:
            link = self.get_test_link(source, target)
            links[link.id_] = link
        return links

    def get_test_link(self, source, target):
        s = Artifact(source, self.TEST_S_ARTS[source], lambda text: text)
        t = Artifact(target, self.TEST_T_ARTS[target], lambda text: text)
        return TraceLink(s, t, lambda text_pair, text, return_token_type_ids, add_special_tokens: text + "_" + text_pair)

    def get_expected_train_dataset_size(self, resample_rate):
        num_train_pos_links = round(len(self.TEST_POS_LINKS) * (1 - self.VAlIDATION_PERCENTAGE))
        return resample_rate * num_train_pos_links * 2  # equal number pos and neg links

    def get_test_trace_dataset_creator(self, validation_percentage=VAlIDATION_PERCENTAGE, include_links=True, model_generator=None):
        if model_generator is None:
            model_generator = self.TEST_MODEL_GENERATOR
        return TraceDatasetCreator(self.TEST_S_ARTS, self.TEST_T_ARTS, model_generator=model_generator,
                                   true_links=self.TEST_POS_LINKS if include_links else None,
                                   validation_percentage=validation_percentage)

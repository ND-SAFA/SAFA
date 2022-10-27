from unittest import mock
from unittest.mock import patch

from test.base_test import BaseTest
from tracer.dataset.data_key import DataKey
from tracer.dataset.data_objects.artifact import Artifact
from tracer.dataset.data_objects.trace_link import TraceLink
from tracer.dataset.trace_dataset import TraceDataset
from tracer.models.model_generator import ModelGenerator
from tracer.models.model_properties import ArchitectureType

FEATURE_VALUE = "({}, {})"


def fake_method(text, text_pair=None, return_token_type_ids=None, add_special_tokens=None):
    return {"feature_" + text: FEATURE_VALUE.format(text, text_pair) if text_pair else text}


class TestTraceDataset(BaseTest):
    VAlIDATION_PERCENTAGE = 0.3
    EXPECTED_VAL_SIZE = 2
    TEST_FEATURE = {"irrelevant_key1": "k",
                    "input_ids": "a",
                    "token_type_ids": "l",
                    "attention_mask": 4}
    FEATURE_KEYS = DataKey.get_feature_entry_keys()
    RESAMPLE_RATE = 3

    @patch.object(ModelGenerator, "get_tokenizer")
    def test_to_trainer_dataset(self, get_tokenizer_mock: mock.MagicMock):
        get_tokenizer_mock.return_value = self.get_test_tokenizer()
        trace_dataset = self.get_trace_dataset()
        model_generator = ModelGenerator(**self.MODEL_GENERATOR_PARAMS)
        trainer_dataset = trace_dataset.to_trainer_dataset(model_generator)
        self.assertTrue(isinstance(trainer_dataset[0], dict))
        self.assertEquals(len(trace_dataset.links), len(trainer_dataset))

    def test_get_source_target_pairs(self):
        trace_dataset = self.get_trace_dataset()

        source_target_pairs = trace_dataset.get_source_target_pairs()
        self.assert_lists_have_the_same_vals(source_target_pairs, self.ALL_TEST_LINKS)

    def test_resize_links_duplicates(self):
        new_length = 5

        trace_dataset = self.get_trace_dataset()

        trace_dataset.resize_pos_links(new_length, include_duplicates=True)
        trace_dataset.resize_neg_links(new_length, include_duplicates=True)

        for link_ids in [trace_dataset.pos_link_ids, trace_dataset.neg_link_ids]:
            self.assertEquals(new_length, len(link_ids))

    def test_resize_links_no_duplicates(self):
        new_length = 2

        trace_dataset = self.get_trace_dataset()

        trace_dataset.resize_pos_links(new_length, include_duplicates=False)
        trace_dataset.resize_neg_links(new_length, include_duplicates=False)

        for link_ids in [trace_dataset.pos_link_ids, trace_dataset.neg_link_ids]:
            self.assertEquals(new_length, len(link_ids))
            self.assertEquals(new_length, len(set(link_ids)))  # no duplicates

    def test_resample_links(self):
        trace_dataset = self.get_trace_dataset()
        expected_pos_links = self.RESAMPLE_RATE * len(trace_dataset.pos_link_ids)
        expected_neg_links = self.RESAMPLE_RATE * len(trace_dataset.neg_link_ids)

        trace_dataset.resample_pos_links(self.RESAMPLE_RATE)
        trace_dataset.resample_neg_links(self.RESAMPLE_RATE)

        self.assertEquals(expected_pos_links, len(trace_dataset.pos_link_ids))
        self.assertEquals(expected_neg_links, len(trace_dataset.neg_link_ids))

    def test_split(self):
        trace_dataset = self.get_trace_dataset()
        split1, split2 = trace_dataset.split(self.VAlIDATION_PERCENTAGE)
        self.assertEquals(len(split1), len(self.POS_LINKS) - self.EXPECTED_VAL_SIZE)
        self.assertEquals(len(split2), self.EXPECTED_VAL_SIZE)
        intersection = set(split1.links.keys()).intersection(set(split2.links.keys()))
        self.assertEquals(intersection, 0)

        for split in [split1, split2]:
            link_ids = split.pos_link_ids + split.neg_link_ids
            self.assert_lists_have_the_same_vals(split.links.keys(), link_ids)

    def test_get_feature_entry(self):
        trace_dataset = self.get_trace_dataset()
        source, target = self.POS_LINKS[0]
        test_link = self.get_test_link(source, target)

        feature_entry_single = trace_dataset._get_feature_entry(test_link, ArchitectureType.SIAMESE, fake_method)
        self.assertIn(test_link.source.token, feature_entry_single.values())
        self.assertIn(test_link.target.token, feature_entry_single.values())
        self.assertIn(DataKey.LABEL_KEY, feature_entry_single)

        feature_entry_single = trace_dataset._get_feature_entry(test_link, ArchitectureType.SIAMESE, fake_method)
        self.assertIn(FEATURE_VALUE.format(source.token, target.token), feature_entry_single.values())
        self.assertIn(DataKey.LABEL_KEY, feature_entry_single)

    def test_extract_feature_info(self):
        feature_info = TraceDataset._extract_feature_info(self.TEST_FEATURE)
        self.assert_lists_have_the_same_vals(feature_info.keys(), self.FEATURE_KEYS)

        prefix = "s_"
        feature_info_prefix = TraceDataset._extract_feature_info(self.TEST_FEATURE, prefix)
        for feature_name in feature_info_prefix.keys():
            self.assertTrue(feature_name.startswith(prefix))

    def test_get_data_split(self):
        split1 = TraceDataset._get_data_split(self.POS_LINKS, self.VAlIDATION_PERCENTAGE, for_second_split=False)
        split2 = TraceDataset._get_data_split(self.POS_LINKS, self.VAlIDATION_PERCENTAGE, for_second_split=True)
        self.assertEquals(len(split1), len(self.POS_LINKS) - self.EXPECTED_VAL_SIZE)
        self.assertEquals(len(split2), self.EXPECTED_VAL_SIZE)
        intersection = set(split1).intersection(set(split2))
        self.assertEquals(len(intersection), 0)

    def test_get_first_split_size(self):
        size = TraceDataset._get_first_split_size(self.POS_LINKS, self.VAlIDATION_PERCENTAGE)
        self.assertEquals(size, len(self.POS_LINKS) - self.EXPECTED_VAL_SIZE)

    def test_prepare_train_split(self):
        pass

    def get_expected_train_dataset_size(self, resample_rate, validation_percentage=VAlIDATION_PERCENTAGE):
        num_train_pos_links = round(len(self.POS_LINKS) * (1 - validation_percentage))
        return resample_rate * num_train_pos_links * 2  # equal number pos and neg links

    def get_trace_dataset(self):
        links = self.get_links(self.ALL_TEST_LINKS)
        pos_links_ids = list(self.get_links(self.POS_LINKS).keys())
        neg_link_ids = list(set(links.keys()).difference(set(pos_links_ids)))
        return TraceDataset(links, pos_links_ids, neg_link_ids)

    def get_links(self, link_list):
        links = {}
        for source, target in link_list:
            link = self.get_test_link(source, target)
            links[link.id] = link
        return links

    def get_test_link(self, source, target):
        s = Artifact(source, self.ALL_TEST_SOURCES[source])
        t = Artifact(target, self.ALL_TEST_TARGETS[target])
        return TraceLink(s, t)

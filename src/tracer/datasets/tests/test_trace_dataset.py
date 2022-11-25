from unittest import mock
from unittest.mock import patch

from test.base_trace_test import BaseTraceTest
from tracer.datasets.creators.csv_dataset_creator import CSVDatasetCreator
from tracer.datasets.data_key import DataKey
from tracer.datasets.processing.augmentation.simple_word_replacement_step import SimpleWordReplacementStep
from tracer.datasets.trace_dataset import TraceDataset
from tracer.models.model_generator import ModelGenerator
from tracer.models.model_properties import ArchitectureType
import pandas as pd

FEATURE_VALUE = "({}, {})"


def fake_synonyms(replacement_word: str, orig_word: str, pos: str):
    if "s_" in orig_word:
        return {replacement_word}
    return set()


def fake_method(text, text_pair=None, return_token_type_ids=None, add_special_tokens=None):
    return {"input_ids": FEATURE_VALUE.format(text, text_pair) if text_pair else text}


class TestTraceDataset(BaseTraceTest):
    VAlIDATION_PERCENTAGE = 0.3
    EXPECTED_VAL_SIZE_NEG_LINKS = round(
        (len(BaseTraceTest.ALL_TEST_LINKS) - len(BaseTraceTest.POS_LINKS)) * VAlIDATION_PERCENTAGE)
    EXPECTED_VAL_SIZE_POS_LINKS = round(len(BaseTraceTest.POS_LINKS) * VAlIDATION_PERCENTAGE)
    TEST_FEATURE = {"irrelevant_key1": "k",
                    "input_ids": "a",
                    "token_type_ids": "l",
                    "attention_mask": 4}
    FEATURE_KEYS = DataKey.get_feature_entry_keys()
    RESAMPLE_RATE = 3

    @patch.object(ModelGenerator, "get_tokenizer")
    def test_to_trainer_dataset(self, get_tokenizer_mock: mock.MagicMock):
        get_tokenizer_mock.return_value = self.get_test_tokenizer()
        train_dataset, test_dataset = self.get_trace_dataset().split(self.VAlIDATION_PERCENTAGE)
        train_dataset.prepare_for_training()
        model_generator = ModelGenerator(**self.MODEL_GENERATOR_PARAMS)
        trainer_dataset = train_dataset.to_trainer_dataset(model_generator)
        self.assertTrue(isinstance(trainer_dataset[0], dict))
        self.assertEquals(self.get_expected_train_dataset_size(resample_rate=1), len(trainer_dataset))

    def test_to_dataframe(self):
        trace_dataset = self.get_trace_dataset()
        df = trace_dataset.to_dataframe()
        self.assertTrue(isinstance(df, pd.DataFrame))
        new_trace_dataset = CSVDatasetCreator("path").create_from_dataframe(data_df=df)
        self.assert_lists_have_the_same_vals(new_trace_dataset.links.keys(), trace_dataset.links.keys())
        self.assert_lists_have_the_same_vals(new_trace_dataset.pos_link_ids, trace_dataset.pos_link_ids)
        self.assert_lists_have_the_same_vals(new_trace_dataset.neg_link_ids, trace_dataset.neg_link_ids)

    @patch.object(SimpleWordReplacementStep, "_get_word_pos")
    @patch.object(SimpleWordReplacementStep, "_get_synonyms")
    def test_augment_pos_links(self, get_synonym_mock, get_word_pos_mock):
        replacement_word = "augmented_source_token"
        get_synonym_mock.side_effect = lambda orig_word, pos: fake_synonyms(replacement_word, orig_word, pos)
        get_word_pos_mock.return_value = "j"
        trace_dataset = self.get_trace_dataset()
        trace_dataset.augment_pos_links([SimpleWordReplacementStep(1, 0.15)])
        n_augmented_links = 0
        self.assertEquals(len(trace_dataset.pos_link_ids), len(trace_dataset.neg_link_ids))
        for link_id, link in trace_dataset.links.items():
            if SimpleWordReplacementStep.get_aug_id() in link.target.id:
                self.assertIn(link_id, trace_dataset.pos_link_ids)
                self.assertEquals(link.source.token, replacement_word)
                self.assertIn("token", link.target.token)
                self.assertIn(SimpleWordReplacementStep.get_aug_id(), link.source.id)
                n_augmented_links += 1
        self.assertEquals(len(self.NEG_LINKS) - len(self.POS_LINKS), n_augmented_links)

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
        expected_val_link_size = (self.EXPECTED_VAL_SIZE_POS_LINKS + self.EXPECTED_VAL_SIZE_NEG_LINKS)
        self.assertEquals(len(split1), len(self.ALL_TEST_LINKS) - expected_val_link_size)
        self.assertEquals(len(split2), expected_val_link_size)
        intersection = set(split1.links.keys()).intersection(set(split2.links.keys()))
        self.assertEquals(len(intersection), 0)

        for split in [split1, split2]:
            link_ids = split.pos_link_ids + split.neg_link_ids
            self.assert_lists_have_the_same_vals(split.links.keys(), link_ids)

    def test_prepare_for_training(self):
        n_pos_links = len(self.POS_LINKS)

        trace_dataset_aug = self.get_trace_dataset()
        trace_dataset_aug.prepare_for_training([SimpleWordReplacementStep(1, 0.15)])
        aug_links = {link_id for link_id in trace_dataset_aug.pos_link_ids if
                     SimpleWordReplacementStep.get_aug_id() in trace_dataset_aug.links[link_id].source.id}
        self.assertEquals(len(aug_links), len(self.NEG_LINKS) - n_pos_links)
        self.assertEquals(len(set(trace_dataset_aug.pos_link_ids)), n_pos_links+len(aug_links))
        self.assertEquals(len(trace_dataset_aug.pos_link_ids), len(trace_dataset_aug.neg_link_ids))

        #TODO test on resample
        # trace_dataset_resample = self.get_trace_dataset()
        # trace_dataset_resample.prepare_for_training([SimpleWordReplacementStep(1, 0.15)])
        # aug_links = {link_id for link_id in trace_dataset_resample.pos_link_ids if
        #              SimpleWordReplacementStep.get_aug_id() in trace_dataset_resample.links[link_id].source.id}
        # self.assertEquals(len(aug_links), 0)
        # self.assertEquals(len(trace_dataset_resample.pos_link_ids), 3 * n_pos_links)
        # self.assertEquals(len(trace_dataset_resample.pos_link_ids), len(trace_dataset_resample.neg_link_ids))

    def test_get_feature_entry(self):
        trace_dataset = self.get_trace_dataset()
        source, target = self.POS_LINKS[0]
        test_link = self.get_test_link(source, target)

        feature_entry_siamese = trace_dataset._get_feature_entry(test_link, ArchitectureType.SIAMESE, fake_method)
        self.assertIn(test_link.source.token, feature_entry_siamese.values())
        self.assertIn(test_link.target.token, feature_entry_siamese.values())
        self.assertIn(DataKey.LABEL_KEY, feature_entry_siamese)

        feature_entry_single = trace_dataset._get_feature_entry(test_link, ArchitectureType.SINGLE, fake_method)
        self.assertIn(FEATURE_VALUE.format(test_link.source.token, test_link.target.token),
                      feature_entry_single.values())
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
        self.assertEquals(len(split1), len(self.POS_LINKS) - self.EXPECTED_VAL_SIZE_POS_LINKS)
        self.assertEquals(len(split2), self.EXPECTED_VAL_SIZE_POS_LINKS)
        intersection = set(split1).intersection(set(split2))
        self.assertEquals(len(intersection), 0)

    def test_get_first_split_size(self):
        size = TraceDataset._get_first_split_size(self.POS_LINKS, self.VAlIDATION_PERCENTAGE)
        self.assertEquals(size, len(self.POS_LINKS) - self.EXPECTED_VAL_SIZE_POS_LINKS)

    def get_trace_dataset(self):
        links = self.get_links(self.ALL_TEST_LINKS)
        pos_links_ids = self.get_link_ids(self.POS_LINKS)
        neg_link_ids = self.get_link_ids(self.NEG_LINKS)
        for link in links.values():
            if link.id in pos_links_ids:
                link.is_true_link = True
        return TraceDataset(links, pos_links_ids, neg_link_ids)

    def get_expected_train_dataset_size(self, resample_rate=RESAMPLE_RATE, validation_percentage=VAlIDATION_PERCENTAGE):
        num_train_pos_links = round(len(self.POS_LINKS) * (1 - validation_percentage))
        return resample_rate * num_train_pos_links * 2  # equal number pos and neg links

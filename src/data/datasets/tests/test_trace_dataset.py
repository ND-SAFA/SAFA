import uuid
from collections import Counter
from unittest import mock
from unittest.mock import patch

from data.datasets.data_key import DataKey
from data.datasets.trace_dataset import TraceDataset
from data.processing.augmentation.abstract_data_augmentation_step import AbstractDataAugmentationStep
from data.processing.augmentation.data_augmenter import DataAugmenter
from data.processing.augmentation.resample_step import ResampleStep
from data.processing.augmentation.simple_word_replacement_step import SimpleWordReplacementStep
from data.processing.augmentation.source_target_swap_step import SourceTargetSwapStep
from data.tree.trace_link import TraceLink
from models.model_manager import ModelManager
from models.model_properties import ModelArchitectureType
from testres.base_trace_test import BaseTraceTest
from testres.test_assertions import TestAssertions
from testres.test_data_manager import TestDataManager

FEATURE_VALUE = "({}, {})"


def fake_synonyms(replacement_word: str, orig_word: str, pos: str):
    if "s_" in orig_word:
        return {replacement_word + str(uuid.uuid4())[:2]}
    return set()


def fake_method(text, text_pair=None, return_token_type_ids=None, add_special_tokens=None):
    return {"input_ids": FEATURE_VALUE.format(text, text_pair) if text_pair else text}


class TestTraceDataset(BaseTraceTest):
    VAlIDATION_PERCENTAGE = 0.3
    N_LINKS = len(TestDataManager.get_all_links())
    N_POSITIVE = len(TestDataManager.get_positive_links())
    N_NEGATIVE = len(TestDataManager.get_negative_links())
    EXPECTED_VAL_SIZE_NEG_LINKS = round((N_LINKS - N_POSITIVE) * VAlIDATION_PERCENTAGE)
    EXPECTED_VAL_SIZE_POS_LINKS = round(N_POSITIVE * VAlIDATION_PERCENTAGE)
    TEST_FEATURE = {"irrelevant_key1": "k",
                    "input_ids": "a",
                    "token_type_ids": "l",
                    "attention_mask": 4}
    FEATURE_KEYS = DataKey.get_feature_entry_keys()
    RESAMPLE_RATE = 3
    positive_links = TestDataManager._create_link_map(TestDataManager.get_positive_links())
    all_links = TestDataManager._create_link_map(TestDataManager.get_all_links())
    negative_links = TestDataManager._create_link_map(TestDataManager.get_negative_links())

    @patch.object(ModelManager, "get_tokenizer")
    def test_to_trainer_dataset(self, get_tokenizer_mock: mock.MagicMock):
        get_tokenizer_mock.return_value = self.get_test_tokenizer()
        train_dataset, test_dataset = self.get_trace_dataset().split(self.VAlIDATION_PERCENTAGE)
        train_dataset.prepare_for_training()
        model_generator = ModelManager(**self.MODEL_MANAGER_PARAMS)
        trainer_dataset = train_dataset.to_trainer_dataset(model_generator)
        self.assertTrue(isinstance(trainer_dataset[0], dict))
        self.assertEquals(self.get_expected_train_dataset_size(resample_rate=1), len(trainer_dataset))

    @patch.object(SimpleWordReplacementStep, "_get_word_pos")
    @patch.object(SimpleWordReplacementStep, "_get_synonyms")
    def test_augment_pos_links(self, get_synonym_mock, get_word_pos_mock):
        replacement_word = "augmented_source_token"
        get_synonym_mock.side_effect = lambda orig_word, pos: fake_synonyms(replacement_word, orig_word, pos)
        get_word_pos_mock.return_value = "j"

        trace_dataset = self.get_trace_dataset()
        trace_dataset.resize_neg_links(44)

        steps = [SimpleWordReplacementStep(0.5, 0.15), SourceTargetSwapStep()]
        step_ids = [step.extract_unique_id_from_step_id(step.get_id()) for step in steps]
        steps.append(ResampleStep(0.5))
        n_expected = [(len(trace_dataset.neg_link_ids) - (2 * len(trace_dataset.pos_link_ids))) * .5,
                      len(trace_dataset.pos_link_ids)]
        n_expected.append(n_expected[0])
        data_augmenter = DataAugmenter(steps)
        trace_dataset.augment_pos_links(data_augmenter)
        self.assertEquals(len(trace_dataset.pos_link_ids), len(trace_dataset.neg_link_ids))

        n_augmented_links = [0 for i in range(len(step_ids))]
        n_overlap = 0
        for link_id, link in trace_dataset.links.items():
            for i, step_id in enumerate(step_ids):
                if step_id in link.target.id:
                    self.assertIn(link_id, trace_dataset.pos_link_ids)
                    self.assertIn(step_id, link.source.id)
                    n_augmented_links[i] += 1
                    if isinstance(steps[i], SimpleWordReplacementStep):
                        if replacement_word not in link.source.token and replacement_word not in link.target.token:
                            self.fail("Did not properly perform simple word replacement")
                        self.assertIn("token", link.target.token)
                    elif isinstance(steps[i], SourceTargetSwapStep):
                        self.assertIn("t_", link.source.token)
                        if "s_" not in link.target.token:
                            if replacement_word not in link.target.token:
                                self.fail("Did not properly perform source target swap")
                            n_overlap += 1
        n_expected[1] += n_overlap

        link_counts = Counter(trace_dataset.pos_link_ids)
        n_resampled = 0
        for count in link_counts.values():
            n_resampled += count - 1
        n_augmented_links.append(n_resampled)
        for i, expected in enumerate(n_expected):
            actual = n_augmented_links[i]
            if expected != actual:
                self.fail("Expected number of links (%d) does not match actual (%d) for %s" % (
                    expected, actual, str(type(steps[i]))))

    def test_add_link(self):
        trace_dataset = self.get_trace_dataset()
        source_tokens, target_tokens = "s_token", "t_token"

        true_source_id, true_target_id = "source_id1", "target_id1"
        trace_dataset.add_link(true_source_id, true_target_id, source_tokens, target_tokens, is_true_link=True)
        true_link_id = TraceLink.generate_link_id(true_source_id, true_target_id)
        self.assertIn(true_link_id, trace_dataset.links)
        self.assertNotIn(true_link_id, trace_dataset.neg_link_ids)
        self.assertIn(true_link_id, trace_dataset.pos_link_ids)
        self.assertEquals(trace_dataset.links[true_link_id].source.token, source_tokens)
        self.assertEquals(trace_dataset.links[true_link_id].target.token, target_tokens)

        false_source_id, false_target_id = "source_id2", "target_id2"
        trace_dataset.add_link(false_source_id, false_target_id, source_tokens, target_tokens, is_true_link=False)
        false_link_id = TraceLink.generate_link_id(false_source_id, false_target_id)
        self.assertIn(false_link_id, trace_dataset.links)
        self.assertIn(false_link_id, trace_dataset.neg_link_ids)
        self.assertNotIn(false_link_id, trace_dataset.pos_link_ids)

    def test_get_augmented_artifact_ids(self):
        trace_dataset = self.get_trace_dataset()
        augmented_tokens = ("s_token_aug", "t_token_aug")
        aug_step_id = "9349jsf"
        entry_num = 1
        orig_link = list(trace_dataset.links.values()).pop()

        aug_source_id, aug_target_id = trace_dataset._get_augmented_artifact_ids(augmented_tokens, orig_link,
                                                                                 aug_step_id, entry_num)
        self.assertEquals(aug_source_id, orig_link.source.id + aug_step_id)
        self.assertEquals(aug_target_id, orig_link.target.id + aug_step_id)

        # link id already exists but is same as augmented
        trace_dataset.add_link(aug_source_id, aug_target_id, *augmented_tokens, is_true_link=True)
        aug_source_id, aug_target_id = trace_dataset._get_augmented_artifact_ids(augmented_tokens, orig_link,
                                                                                 aug_step_id, entry_num)
        self.assertEquals(aug_source_id, orig_link.source.id + aug_step_id)
        self.assertEquals(aug_target_id, orig_link.target.id + aug_step_id)

        # link id already exists but is NOT the same as augmented
        trace_dataset.add_link(aug_source_id, aug_target_id, "s_token", "t_token", is_true_link=True)
        aug_source_id, aug_target_id = trace_dataset._get_augmented_artifact_ids(augmented_tokens, orig_link,
                                                                                 aug_step_id, entry_num)
        self.assertEquals(aug_source_id, orig_link.source.id + aug_step_id + str(entry_num))
        self.assertEquals(aug_target_id, orig_link.target.id + aug_step_id + str(entry_num))

    def test_get_data_entries_for_augmentation(self):
        trace_dataset = self.get_trace_dataset()
        pos_links, data_entries = trace_dataset._get_data_entries_for_augmentation()
        TestAssertions.assert_lists_have_the_same_vals(self, [link.id for link in pos_links],
                                                       [link.id for link in self.positive_links.values()])
        self.assertEquals(len(data_entries), self.N_POSITIVE)
        for link_id, link in self.positive_links.items():
            source_body = TestDataManager._get_artifact_body(link.source.id)
            target_body = TestDataManager._get_artifact_body(link.target.id)
            self.assertIn((source_body, target_body), data_entries)

    def test_create_links_from_augmentation(self):
        ids = ['id1', 'id2']
        orig_links = list(self.positive_links.values())
        base_result = [(link.source.token, link.target.token) for link in orig_links]
        results = [[(id_ + pair[0], id_ + pair[1]) for pair in base_result] for id_ in ids]
        augmentation_results = {
            AbstractDataAugmentationStep.COMMON_ID + id_: zip(results[i], [j for j in range(len(orig_links))])
            for i, id_ in enumerate(ids)}
        trace_dataset = self.get_trace_dataset()
        trace_dataset._create_links_from_augmentation(augmentation_results, orig_links)
        self.assertEquals(len(trace_dataset.pos_link_ids), 3 * len(orig_links))
        n_augmented_links = [0 for i in range(len(ids))]
        for link in trace_dataset.links.values():
            for i, id_ in enumerate(ids):
                if id_ in link.source.id:
                    self.assertIn(id_, link.target.id)
                    self.assertIn(id_, link.source.token)
                    self.assertIn(id_, link.target.token)
                    self.assertIn(link.id, trace_dataset.pos_link_ids)
                    n_augmented_links[i] += 1
        for count in n_augmented_links:
            self.assertEquals(count, len(orig_links))

    def test_get_source_target_pairs(self):
        trace_dataset = self.get_trace_dataset()

        source_target_pairs = trace_dataset.get_source_target_pairs()
        expected_pairs = TestDataManager.get_all_links()
        TestAssertions.assert_lists_have_the_same_vals(self, source_target_pairs, expected_pairs)

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

    def test_split(self):
        trace_dataset = self.get_trace_dataset()
        split1, split2 = trace_dataset.split(self.VAlIDATION_PERCENTAGE)
        expected_val_link_size = (self.EXPECTED_VAL_SIZE_POS_LINKS + self.EXPECTED_VAL_SIZE_NEG_LINKS)
        self.assertEquals(len(split1), len(self.all_links) - expected_val_link_size)
        self.assertEquals(len(split2), expected_val_link_size)
        intersection = set(split1.links.keys()).intersection(set(split2.links.keys()))
        self.assertEquals(len(intersection), 0)

        for split in [split1, split2]:
            link_ids = split.pos_link_ids + split.neg_link_ids
            TestAssertions.assert_lists_have_the_same_vals(self, split.links.keys(), link_ids)

    def test_split_multiple(self):
        trace_dataset = self.get_trace_dataset()
        n_orig_links = len(trace_dataset)
        percent_splits = [0.3, 0.2]
        splits = trace_dataset.split_multiple(percent_splits)
        length_of_splits = [len(split) for split in splits]
        split_link_ids = [set(split.links.keys()) for split in splits]
        self.assertEquals(sum(length_of_splits), n_orig_links)
        for i, len_split in enumerate(length_of_splits):
            if i == 0:
                self.assertLessEqual(abs(len_split - round(n_orig_links * (1 - sum(percent_splits)))), 1)
                continue
            self.assertLessEqual(abs(len_split - round(n_orig_links * percent_splits[i - 1])), 1)
        for i, split in enumerate(splits):
            link_ids = split_link_ids[i]
            for j, other_link_ids in enumerate(split_link_ids):
                if i == j:
                    continue
                intersection = other_link_ids.intersection(link_ids)
                self.assertEquals(len(intersection), 0)

    def test_prepare_for_training(self):

        trace_dataset_aug = self.get_trace_dataset()
        data_augmenter = DataAugmenter([SimpleWordReplacementStep(1, 0.15)])
        trace_dataset_aug.prepare_for_training(data_augmenter)
        aug_links = {link_id for link_id in trace_dataset_aug.pos_link_ids if
                     AbstractDataAugmentationStep.extract_unique_id_from_step_id(SimpleWordReplacementStep.get_id())
                     in trace_dataset_aug.links[link_id].source.id}
        self.assertEquals(len(aug_links), self.N_NEGATIVE - self.N_POSITIVE)
        self.assertEquals(len(set(trace_dataset_aug.pos_link_ids)), self.N_POSITIVE + len(aug_links))
        self.assertEquals(len(trace_dataset_aug.pos_link_ids), len(trace_dataset_aug.neg_link_ids))

    def test_get_feature_entry(self):
        trace_dataset = self.get_trace_dataset()
        source, target = TestDataManager.get_positive_links()[0]
        test_link = TestDataManager._create_test_link(source, target)

        feature_entry_siamese = trace_dataset._get_feature_entry(test_link, ModelArchitectureType.SIAMESE, fake_method)
        self.assertIn(test_link.source.token, feature_entry_siamese.values())
        self.assertIn(test_link.target.token, feature_entry_siamese.values())
        self.assertIn(DataKey.LABEL_KEY, feature_entry_siamese)

        feature_entry_single = trace_dataset._get_feature_entry(test_link, ModelArchitectureType.SINGLE, fake_method)
        self.assertIn(FEATURE_VALUE.format(test_link.source.token, test_link.target.token),
                      feature_entry_single.values())
        self.assertIn(DataKey.LABEL_KEY, feature_entry_single)

    def test_extract_feature_info(self):
        feature_info = TraceDataset._extract_feature_info(self.TEST_FEATURE)
        TestAssertions.assert_lists_have_the_same_vals(self, feature_info.keys(), self.FEATURE_KEYS)

        prefix = "s_"
        feature_info_prefix = TraceDataset._extract_feature_info(self.TEST_FEATURE, prefix)
        for feature_name in feature_info_prefix.keys():
            self.assertTrue(feature_name.startswith(prefix))

    def test_get_data_split(self):
        positive_links = list(self.positive_links.values())
        split1 = TraceDataset._get_data_split(positive_links, self.VAlIDATION_PERCENTAGE, for_second_split=False)
        split2 = TraceDataset._get_data_split(positive_links, self.VAlIDATION_PERCENTAGE, for_second_split=True)
        self.assertEquals(len(split1), self.N_POSITIVE - self.EXPECTED_VAL_SIZE_POS_LINKS)
        self.assertEquals(len(split2), self.EXPECTED_VAL_SIZE_POS_LINKS)
        intersection = set(split1).intersection(set(split2))
        self.assertEquals(len(intersection), 0)

    def test_get_first_split_size(self):
        size = TraceDataset._get_first_split_size(TestDataManager.get_positive_links(), self.VAlIDATION_PERCENTAGE)
        self.assertEquals(size, self.N_POSITIVE - self.EXPECTED_VAL_SIZE_POS_LINKS)

    def get_trace_dataset(self):
        links = TestDataManager._create_link_map(TestDataManager.get_all_links())
        pos_links_ids = TestDataManager.get_positive_link_ids()
        for link in links.values():
            if link.id in pos_links_ids:
                link.is_true_link = True
        return TraceDataset(links)

    def get_expected_train_dataset_size(self, resample_rate=RESAMPLE_RATE, validation_percentage=VAlIDATION_PERCENTAGE):
        num_train_pos_links = round(self.N_POSITIVE * (1 - validation_percentage))
        return resample_rate * num_train_pos_links * 2  # equal number pos and neg links

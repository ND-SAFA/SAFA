import os
import uuid
from collections import Counter
from unittest.mock import patch

from common_resources.data.dataframes.trace_dataframe import TraceDataFrame
from common_resources.data.keys.csv_keys import CSVKeys
from common_resources.data.keys.structure_keys import ArtifactKeys, TraceKeys
from common_resources.data.processing.augmentation.abstract_data_augmentation_step import AbstractDataAugmentationStep
from common_resources.data.processing.augmentation.data_augmenter import DataAugmenter
from common_resources.data.processing.augmentation.resample_step import ResampleStep
from common_resources.data.processing.augmentation.simple_word_replacement_step import SimpleWordReplacementStep
from common_resources.data.processing.augmentation.source_target_swap_step import SourceTargetSwapStep
from common_resources.data.tdatasets.data_key import DataKey
from common_resources.data.tdatasets.trace_dataset import TraceDataset
from tgen.models.model_properties import ModelArchitectureType
from tgen.testres.base_tests.base_trace_test import BaseTraceTest
from tgen.testres.paths.paths import TEST_OUTPUT_DIR
from tgen.testres.test_assertions import TestAssertions
from tgen.testres.test_data_manager import TestDataManager
from tgen.testres.testprojects.api_test_project import ApiTestProject

FEATURE_VALUE = "({}, {})"


def fake_synonyms(replacement_word: str, orig_word: str, pos: str):
    if "s_" in orig_word:
        return {replacement_word + str(uuid.uuid4())[:2]}
    return set()


def fake_method(text, text_pair=None, return_token_type_ids=None, add_special_tokens=None):
    return {"input_ids": FEATURE_VALUE.format(text, text_pair) if text_pair else text}


class TestTraceDataset(BaseTraceTest):
    TEST_FEATURE = {"irrelevant_key1": "k",
                    "input_ids": "a",
                    "token_type_ids": "l",
                    "attention_mask": 4}
    FEATURE_KEYS = DataKey.get_feature_entry_keys()

    @patch.object(SimpleWordReplacementStep, "_get_word_pos")
    @patch.object(SimpleWordReplacementStep, "_get_synonyms")
    def test_augment_pos_links(self, get_synonym_mock, get_word_pos_mock):
        replacement_word = "augmented_source_token"
        get_synonym_mock.side_effect = lambda orig_word, pos: fake_synonyms(replacement_word, orig_word, pos)
        get_word_pos_mock.return_value = "j"

        trace_dataset = self.get_trace_dataset()

        steps = [SimpleWordReplacementStep(0.5, 0.15), SourceTargetSwapStep()]
        steps.append(ResampleStep(0.5))
        n_negative = len(trace_dataset.get_neg_link_ids())
        n_positive = len(trace_dataset.get_pos_link_ids())
        n_expected = [(n_negative - (2 * n_positive)) * .5, n_positive]
        n_expected.append(n_expected[0])
        data_augmenter = DataAugmenter(steps)
        trace_dataset.augment_pos_links(data_augmenter)
        n_negative = len(trace_dataset.get_neg_link_ids())
        n_positive = len(trace_dataset.get_pos_link_ids())
        self.assertEqual(n_positive, n_negative)

        step_ids = [step.extract_unique_id_from_step_id(step.get_id()) for step in steps[:2]]
        n_augmented_links = [0 for i in range(len(step_ids))]
        n_overlap = 0
        for link_id, link in trace_dataset.trace_df.itertuples():
            child_id, parent_id = link[TraceKeys.SOURCE], link[TraceKeys.TARGET]
            child_content = trace_dataset.artifact_df.get_artifact(child_id)[ArtifactKeys.CONTENT]
            parent_content = trace_dataset.artifact_df.get_artifact(parent_id)[ArtifactKeys.CONTENT]
            for i, step_id in enumerate(step_ids):
                if step_id in parent_id:
                    self.assertIn(step_id, child_id)
                    n_augmented_links[i] += 1
                    if isinstance(steps[i], SimpleWordReplacementStep):
                        if replacement_word not in child_content \
                                and replacement_word not in parent_content:
                            self.fail("Did not properly perform simple word replacement")
                        self.assertIn("token", parent_content)
                    elif isinstance(steps[i], SourceTargetSwapStep):
                        self.assertIn("t_", child_content)
                        if "s_" not in parent_content:
                            if replacement_word not in parent_content:
                                self.fail("Did not properly perform source target swap")
                            n_overlap += 1
        n_expected[1] += n_overlap

        link_counts = Counter(trace_dataset.get_pos_link_ids())
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

        trace_dataset.trace_df.add_link(source=true_source_id, target=true_target_id, )
        trace_dataset.create_and_add_link(true_source_id, true_target_id, source_tokens, target_tokens, is_true_link=True)
        true_link_id = TraceDataFrame.generate_link_id(true_source_id, true_target_id)
        self.assertIn(true_link_id, trace_dataset.trace_df.index)
        self.assertNotIn(true_link_id, trace_dataset.get_neg_link_ids())
        self.assertIn(true_link_id, trace_dataset.get_pos_link_ids())
        source, target = trace_dataset.get_link_source_target_artifact(true_link_id)
        self.assertEqual(source[ArtifactKeys.CONTENT], source_tokens)
        self.assertEqual(target[ArtifactKeys.CONTENT], target_tokens)

        false_source_id, false_target_id = "source_id2", "target_id2"
        trace_dataset.create_and_add_link(false_source_id, false_target_id, source_tokens, target_tokens, is_true_link=False)
        false_link_id = TraceDataFrame.generate_link_id(false_source_id, false_target_id)
        self.assertIn(false_link_id, trace_dataset.trace_df.index)
        self.assertIn(false_link_id, trace_dataset.get_neg_link_ids())
        self.assertNotIn(false_link_id, trace_dataset.get_pos_link_ids())

    def test_get_augmented_artifact_ids(self):
        trace_dataset = self.get_trace_dataset()
        augmented_tokens = ("s_token_aug", "t_token_aug")
        aug_step_id = "9349jsf"
        entry_num = 1
        orig_link = trace_dataset.trace_df.get_link(trace_dataset.trace_df.index[0])

        aug_source_id, aug_target_id = trace_dataset._get_augmented_artifact_ids(augmented_tokens, orig_link[TraceKeys.LINK_ID],
                                                                                 aug_step_id, entry_num)
        self.assertEqual(aug_source_id, orig_link[TraceKeys.SOURCE] + aug_step_id)
        self.assertEqual(aug_target_id, orig_link[TraceKeys.TARGET] + aug_step_id)

        # link id already exists but is same as augmented
        trace_dataset = self.get_trace_dataset()
        trace_dataset.create_and_add_link(aug_source_id, aug_target_id, *augmented_tokens, is_true_link=True)
        aug_source_id, aug_target_id = trace_dataset._get_augmented_artifact_ids(augmented_tokens, orig_link[TraceKeys.LINK_ID],
                                                                                 aug_step_id, entry_num)
        self.assertEqual(aug_source_id, orig_link[TraceKeys.SOURCE] + aug_step_id)
        self.assertEqual(aug_target_id, orig_link[TraceKeys.TARGET] + aug_step_id)

        # link id already exists but is NOT the same as augmented
        trace_dataset = self.get_trace_dataset()
        trace_dataset.create_and_add_link(aug_source_id, aug_target_id, "s_token", "t_token", is_true_link=True)
        aug_source_id, aug_target_id = trace_dataset._get_augmented_artifact_ids(augmented_tokens, orig_link[TraceKeys.LINK_ID],
                                                                                 aug_step_id, entry_num)
        self.assertEqual(aug_source_id, orig_link[TraceKeys.SOURCE] + aug_step_id + str(entry_num))
        self.assertEqual(aug_target_id, orig_link[TraceKeys.TARGET] + aug_step_id + str(entry_num))

    def test_get_data_entries_for_augmentation(self):
        trace_dataset = self.get_trace_dataset()
        pos_links, data_entries = trace_dataset._get_data_entries_for_augmentation()
        TestAssertions.assert_lists_have_the_same_vals(self, pos_links,
                                                       list(self.positive_links.index))
        self.assertEqual(len(data_entries), self.N_POSITIVE)
        for link_id, link in self.positive_links.itertuples():
            source_body = TestDataManager.get_artifact_body(link[TraceKeys.SOURCE])
            target_body = TestDataManager.get_artifact_body(link[TraceKeys.TARGET])
            self.assertIn((source_body, target_body), data_entries)

    def test_create_links_from_augmentation(self):
        ids = ['id1', 'id2']
        orig_links = self.positive_links
        base_result = [(link[TraceKeys.SOURCE], link[TraceKeys.TARGET]) for index, link in orig_links.itertuples()]
        results = [[(id_ + pair[0], id_ + pair[1]) for pair in base_result] for id_ in ids]
        augmentation_results = {
            AbstractDataAugmentationStep.COMMON_ID + id_: zip(results[i], [j for j in range(len(orig_links))])
            for i, id_ in enumerate(ids)}
        trace_dataset = self.get_trace_dataset()
        trace_dataset._create_links_from_augmentation(augmentation_results,
                                                      list(orig_links.index))
        self.assertEqual(len(trace_dataset.get_pos_link_ids()), 3 * len(orig_links))
        n_augmented_links = [0 for i in range(len(ids))]
        for index, link in trace_dataset.trace_df.itertuples():
            for i, id_ in enumerate(ids):
                source_id, target_id = link[TraceKeys.SOURCE], link[TraceKeys.TARGET]
                if id_ in source_id:
                    self.assertIn(id_, target_id)
                    source_content = trace_dataset.artifact_df.get_artifact(source_id)[ArtifactKeys.CONTENT]
                    target_content = trace_dataset.artifact_df.get_artifact(target_id)[ArtifactKeys.CONTENT]
                    self.assertIn(id_, source_content)
                    self.assertIn(id_, target_content)
                    self.assertIn(index, trace_dataset.get_pos_link_ids())
                    n_augmented_links[i] += 1

        for count in n_augmented_links:
            self.assertEqual(count, len(orig_links))

    def test_get_source_target_pairs(self):
        trace_dataset = self.get_trace_dataset()

        source_target_pairs = trace_dataset.get_source_target_pairs()
        expected_pairs = ApiTestProject.get_expected_links()
        TestAssertions.assert_lists_have_the_same_vals(self, source_target_pairs, expected_pairs)

        random_order = list(trace_dataset.trace_df.index)
        source_target_pairs = trace_dataset.get_source_target_pairs(random_order)
        self.assertEqual(len(random_order), len(source_target_pairs))
        for i, link_id in enumerate(random_order):
            link = trace_dataset.trace_df.get_link(link_id)
            self.assertEqual(source_target_pairs[i], (link[TraceKeys.SOURCE], link[TraceKeys.TARGET]))

    def test_resize_links_duplicates(self):
        new_length = 5

        trace_dataset = self.get_trace_dataset()

        trace_dataset.resize_pos_links(new_length, include_duplicates=True)
        trace_dataset.resize_neg_links(new_length, include_duplicates=True)

        n_positive = len(trace_dataset.get_pos_link_ids())
        n_negative = len(trace_dataset.get_neg_link_ids())

        self.assertEqual(new_length, n_positive)
        self.assertEqual(new_length, n_negative)

    def test_resize_links_no_duplicates(self):
        new_length = 2

        trace_dataset = self.get_trace_dataset()

        trace_dataset.resize_pos_links(new_length, include_duplicates=False)
        trace_dataset.resize_neg_links(new_length, include_duplicates=False)

        for link_ids in [trace_dataset.get_pos_link_ids(), trace_dataset.get_neg_link_ids()]:
            self.assertEqual(new_length, len(link_ids))
            self.assertEqual(new_length, len(set(link_ids)))  # no duplicates

    def test_augmented_links_for_training(self):
        trace_dataset_aug = self.get_trace_dataset()
        data_augmenter = DataAugmenter([SimpleWordReplacementStep(1, 0.15)])
        trace_dataset_aug.prepare_for_training(data_augmenter)
        aug_links = {link_id for link_id in trace_dataset_aug.get_pos_link_ids() if
                     AbstractDataAugmentationStep.extract_unique_id_from_step_id(SimpleWordReplacementStep.get_id())
                     in trace_dataset_aug.trace_df.get_link(link_id)[TraceKeys.SOURCE]}
        self.assertEqual(len(aug_links), self.N_NEGATIVE - self.N_POSITIVE)
        self.assertEqual(len(set(trace_dataset_aug.get_pos_link_ids())), self.N_POSITIVE + len(aug_links))
        self.assertEqual(len(trace_dataset_aug.get_pos_link_ids()), len(trace_dataset_aug.get_neg_link_ids()))

    def test_get_feature_entry_siamese(self):
        trace_dataset, test_link, source_text, target_text = self.get_single_testing_link()
        input_example = trace_dataset._get_feature_entry(ModelArchitectureType.SIAMESE, None, link_id=test_link[TraceKeys.LINK_ID])
        feature_s_text = input_example[CSVKeys.SOURCE]
        feature_t_text = input_example[CSVKeys.TARGET]
        self.assertEqual(source_text, feature_s_text)
        self.assertEqual(target_text, feature_t_text)
        self.assertEqual(test_link[TraceKeys.LABEL], input_example[CSVKeys.LABEL])

    def test_get_feature_entry_single(self):
        trace_dataset, test_link, source_text, target_text = self.get_single_testing_link()
        feature_entry_single = trace_dataset._get_feature_entry(ModelArchitectureType.SINGLE, fake_method,
                                                                link_id=test_link[TraceKeys.LINK_ID])
        self.assertIn(FEATURE_VALUE.format(source_text, target_text), feature_entry_single.values())
        self.assertIn(DataKey.LABEL_KEY, feature_entry_single)

    def test_extract_feature_info(self):
        feature_info = TraceDataset._extract_feature_info(self.TEST_FEATURE)
        TestAssertions.assert_lists_have_the_same_vals(self, feature_info.keys(), self.FEATURE_KEYS)

        prefix = "s_"
        feature_info_prefix = TraceDataset._extract_feature_info(self.TEST_FEATURE, prefix)
        for feature_name in feature_info_prefix.keys():
            self.assertTrue(feature_name.startswith(prefix))

    def test_as_creator(self):
        trace_dataset = self.get_trace_dataset()
        creator = trace_dataset.as_creator(os.path.join(TEST_OUTPUT_DIR, "dir1"))
        recreated_dataset = creator.create()
        self.assertEqual(set(recreated_dataset.artifact_df.index), set(trace_dataset.artifact_df.index))
        for i, link in trace_dataset.trace_df.itertuples():
            self.assertIsNotNone(recreated_dataset.trace_df.get_link(source_id=link[TraceKeys.SOURCE],
                                                                     target_id=link[TraceKeys.TARGET]))

    def get_single_testing_link(self):
        trace_dataset = self.get_trace_dataset()

        source, target = ApiTestProject.get_positive_links()[0]
        test_link = trace_dataset.trace_df.get_link(source_id=source, target_id=target)
        source_text = trace_dataset.artifact_df.get_artifact(source)[ArtifactKeys.CONTENT]
        target_text = trace_dataset.artifact_df.get_artifact(target)[ArtifactKeys.CONTENT]
        return trace_dataset, test_link, source_text, target_text

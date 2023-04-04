import uuid
from collections import Counter
from unittest import mock
from unittest.mock import patch

from tgen.data.dataframes.artifact_dataframe import ArtifactKeys
from tgen.data.tdatasets.data_key import DataKey
from tgen.data.tdatasets.trace_dataset import TraceDataset
from tgen.data.processing.augmentation.abstract_data_augmentation_step import AbstractDataAugmentationStep
from tgen.data.processing.augmentation.data_augmenter import DataAugmenter
from tgen.data.processing.augmentation.resample_step import ResampleStep
from tgen.data.processing.augmentation.simple_word_replacement_step import SimpleWordReplacementStep
from tgen.data.processing.augmentation.source_target_swap_step import SourceTargetSwapStep
from tgen.data.dataframes.trace_dataframe import TraceDataFrame, TraceKeys
from tgen.models.model_manager import ModelManager
from tgen.models.model_properties import ModelArchitectureType
from test.testres.base_trace_test import BaseTraceTest
from test.testres.test_assertions import TestAssertions
from test.testres.test_data_manager import TestDataManager
from test.testres.testprojects.api_test_project import ApiTestProject

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
        for link_id, link in trace_dataset.trace_df.iterrows():
            source_id, target_id = link[TraceKeys.SOURCE.value], link[TraceKeys.TARGET.value]
            source_content = trace_dataset.artifact_df.get_artifact(source_id)[ArtifactKeys.CONTENT]
            target_content = trace_dataset.artifact_df.get_artifact(target_id)[ArtifactKeys.CONTENT]
            for i, step_id in enumerate(step_ids):
                if step_id in target_id:
                    self.assertIn(link_id, trace_dataset.pos_link_ids)
                    self.assertIn(step_id, source_id)
                    n_augmented_links[i] += 1
                    if isinstance(steps[i], SimpleWordReplacementStep):
                        if replacement_word not in source_content \
                                and replacement_word not in target_content:
                            self.fail("Did not properly perform simple word replacement")
                        self.assertIn("token", target_content)
                    elif isinstance(steps[i], SourceTargetSwapStep):
                        self.assertIn("t_", source_content)
                        if "s_" not in target_content:
                            if replacement_word not in target_content:
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
        trace_dataset.create_and_add_link(true_source_id, true_target_id, source_tokens, target_tokens, is_true_link=True)
        true_link_id = TraceDataFrame.generate_link_id(true_source_id, true_target_id)
        self.assertIn(true_link_id, trace_dataset.trace_df.index)
        self.assertNotIn(true_link_id, trace_dataset.neg_link_ids)
        self.assertIn(true_link_id, trace_dataset.pos_link_ids)
        source, target = trace_dataset.get_link_source_target_artifact(true_link_id)
        self.assertEquals(source[ArtifactKeys.CONTENT], source_tokens)
        self.assertEquals(target[ArtifactKeys.CONTENT], target_tokens)

        false_source_id, false_target_id = "source_id2", "target_id2"
        trace_dataset.create_and_add_link(false_source_id, false_target_id, source_tokens, target_tokens, is_true_link=False)
        false_link_id = TraceDataFrame.generate_link_id(false_source_id, false_target_id)
        self.assertIn(false_link_id, trace_dataset.trace_df.index)
        self.assertIn(false_link_id, trace_dataset.neg_link_ids)
        self.assertNotIn(false_link_id, trace_dataset.pos_link_ids)

    def test_get_augmented_artifact_ids(self):
        trace_dataset = self.get_trace_dataset()
        augmented_tokens = ("s_token_aug", "t_token_aug")
        aug_step_id = "9349jsf"
        entry_num = 1
        orig_link = trace_dataset.trace_df.get_link(trace_dataset.trace_df.index[0])

        aug_source_id, aug_target_id = trace_dataset._get_augmented_artifact_ids(augmented_tokens, orig_link[TraceKeys.LINK_ID],
                                                                                 aug_step_id, entry_num)
        self.assertEquals(aug_source_id, orig_link[TraceKeys.SOURCE] + aug_step_id)
        self.assertEquals(aug_target_id, orig_link[TraceKeys.TARGET] + aug_step_id)

        # link id already exists but is same as augmented
        trace_dataset = self.get_trace_dataset()
        trace_dataset.create_and_add_link(aug_source_id, aug_target_id, *augmented_tokens, is_true_link=True)
        aug_source_id, aug_target_id = trace_dataset._get_augmented_artifact_ids(augmented_tokens, orig_link[TraceKeys.LINK_ID],
                                                                                 aug_step_id, entry_num)
        self.assertEquals(aug_source_id, orig_link[TraceKeys.SOURCE] + aug_step_id)
        self.assertEquals(aug_target_id, orig_link[TraceKeys.TARGET] + aug_step_id)

        # link id already exists but is NOT the same as augmented
        trace_dataset = self.get_trace_dataset()
        trace_dataset.create_and_add_link(aug_source_id, aug_target_id, "s_token", "t_token", is_true_link=True)
        aug_source_id, aug_target_id = trace_dataset._get_augmented_artifact_ids(augmented_tokens, orig_link[TraceKeys.LINK_ID],
                                                                                 aug_step_id, entry_num)
        self.assertEquals(aug_source_id, orig_link[TraceKeys.SOURCE] + aug_step_id + str(entry_num))
        self.assertEquals(aug_target_id, orig_link[TraceKeys.TARGET] + aug_step_id + str(entry_num))

    def test_get_data_entries_for_augmentation(self):
        trace_dataset = self.get_trace_dataset()
        pos_links, data_entries = trace_dataset._get_data_entries_for_augmentation()
        TestAssertions.assert_lists_have_the_same_vals(self, pos_links,
                                                       list(self.positive_links.index))
        self.assertEquals(len(data_entries), self.N_POSITIVE)
        for link_id, link in self.positive_links.iterrows():
            source_body = TestDataManager._get_artifact_body(link[TraceKeys.SOURCE.value])
            target_body = TestDataManager._get_artifact_body(link[TraceKeys.TARGET.value])
            self.assertIn((source_body, target_body), data_entries)

    def test_create_links_from_augmentation(self):
        ids = ['id1', 'id2']
        orig_links = self.positive_links
        base_result = [(link[TraceKeys.SOURCE.value], link[TraceKeys.TARGET.value]) for index, link in orig_links.iterrows()]
        results = [[(id_ + pair[0], id_ + pair[1]) for pair in base_result] for id_ in ids]
        augmentation_results = {
            AbstractDataAugmentationStep.COMMON_ID + id_: zip(results[i], [j for j in range(len(orig_links))])
            for i, id_ in enumerate(ids)}
        trace_dataset = self.get_trace_dataset()
        trace_dataset._create_links_from_augmentation(augmentation_results,
                                                      list(orig_links.index))
        self.assertEquals(len(trace_dataset.pos_link_ids), 3 * len(orig_links))
        n_augmented_links = [0 for i in range(len(ids))]
        for index, link in trace_dataset.trace_df.iterrows():
            for i, id_ in enumerate(ids):
                source_id, target_id = link[TraceKeys.SOURCE.value], link[TraceKeys.TARGET.value]
                if id_ in source_id:
                    self.assertIn(id_, target_id)
                    source_content = trace_dataset.artifact_df.get_artifact(source_id)[ArtifactKeys.CONTENT]
                    target_content = trace_dataset.artifact_df.get_artifact(target_id)[ArtifactKeys.CONTENT]
                    self.assertIn(id_, source_content)
                    self.assertIn(id_, target_content)
                    self.assertIn(index, trace_dataset.pos_link_ids)
                    n_augmented_links[i] += 1
        for count in n_augmented_links:
            self.assertEquals(count, len(orig_links))

    def test_get_source_target_pairs(self):
        trace_dataset = self.get_trace_dataset()

        source_target_pairs = trace_dataset.get_source_target_pairs()
        expected_pairs = ApiTestProject.get_expected_links()
        TestAssertions.assert_lists_have_the_same_vals(self, source_target_pairs, expected_pairs)

        random_order = list(trace_dataset.trace_df.index)
        source_target_pairs = trace_dataset.get_source_target_pairs(random_order)
        self.assertEquals(len(random_order), len(source_target_pairs))
        for i, link_id in enumerate(random_order):
            link = trace_dataset.trace_df.get_link(link_id)
            self.assertEquals(source_target_pairs[i], (link[TraceKeys.SOURCE], link[TraceKeys.TARGET]))

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

    def test_prepare_for_training(self):
        trace_dataset_aug = self.get_trace_dataset()
        data_augmenter = DataAugmenter([SimpleWordReplacementStep(1, 0.15)])
        trace_dataset_aug.prepare_for_training(data_augmenter)
        aug_links = {link_id for link_id in trace_dataset_aug.pos_link_ids if
                     AbstractDataAugmentationStep.extract_unique_id_from_step_id(SimpleWordReplacementStep.get_id())
                     in trace_dataset_aug.trace_df.get_link(link_id)[TraceKeys.SOURCE]}
        self.assertEquals(len(aug_links), self.N_NEGATIVE - self.N_POSITIVE)
        self.assertEquals(len(set(trace_dataset_aug.pos_link_ids)), self.N_POSITIVE + len(aug_links))
        self.assertEquals(len(trace_dataset_aug.pos_link_ids), len(trace_dataset_aug.neg_link_ids))

    def test_get_feature_entry(self):
        trace_dataset = self.get_trace_dataset()
        source, target = ApiTestProject.get_positive_links()[0]
        test_link = TestDataManager._create_test_link(TraceDataFrame(), source, target)

        feature_entry_siamese = trace_dataset._get_feature_entry(test_link[TraceKeys.LINK_ID], ModelArchitectureType.SIAMESE,
                                                                 fake_method)
        source, target = trace_dataset.get_link_source_target_artifact(test_link[TraceKeys.LINK_ID])
        self.assertIn(source[ArtifactKeys.CONTENT], feature_entry_siamese.values())
        self.assertIn(target[ArtifactKeys.CONTENT], feature_entry_siamese.values())
        self.assertIn(DataKey.LABEL_KEY, feature_entry_siamese)

        feature_entry_single = trace_dataset._get_feature_entry(test_link[TraceKeys.LINK_ID], ModelArchitectureType.SINGLE, fake_method)
        self.assertIn(FEATURE_VALUE.format(source[ArtifactKeys.CONTENT], target[ArtifactKeys.CONTENT]),
                      feature_entry_single.values())
        self.assertIn(DataKey.LABEL_KEY, feature_entry_single)

    def test_extract_feature_info(self):
        feature_info = TraceDataset._extract_feature_info(self.TEST_FEATURE)
        TestAssertions.assert_lists_have_the_same_vals(self, feature_info.keys(), self.FEATURE_KEYS)

        prefix = "s_"
        feature_info_prefix = TraceDataset._extract_feature_info(self.TEST_FEATURE, prefix)
        for feature_name in feature_info_prefix.keys():
            self.assertTrue(feature_name.startswith(prefix))

    @patch.object(ModelManager, "get_tokenizer")
    def test_to_trainer_dataset(self, get_tokenizer_mock: mock.MagicMock):
        get_tokenizer_mock.return_value = self.get_test_tokenizer()
        train_dataset = self.get_trace_dataset()
        model_generator = ModelManager(**self.MODEL_MANAGER_PARAMS)
        trainer_dataset = train_dataset.to_trainer_dataset(model_generator)
        self.assertTrue(isinstance(trainer_dataset[0], dict))
        self.assertEquals(len(train_dataset), len(trainer_dataset))

from test.base_test import BaseTest
from tracer.datasets.processing.augmentation.data_augmenter import DataAugmenter
from tracer.datasets.processing.augmentation.resample_step import ResampleStep
from tracer.datasets.processing.augmentation.simple_word_replacement_step import SimpleWordReplacementStep
from tracer.datasets.processing.augmentation.source_target_swap_step import SourceTargetSwapStep


class TestDataAugmenter(BaseTest):
    STEPS = [SourceTargetSwapStep(), ResampleStep(.5), SimpleWordReplacementStep(.5)]

    def test_run(self):
        data_entries = [("0", "1"), ("2", "3")]
        augmenter = self.get_data_augmenter()
        results = augmenter.run(data_entries, n_total_expected=10, include_all_but_step_type=SourceTargetSwapStep)
        self.assertFalse(self.STEPS[0].get_aug_id() in results)
        self.assertEquals(len(results), len(self.STEPS[1:]))
        for step in self.STEPS[1:]:
            id_ = step.get_aug_id()
            self.assertIn(id_, results)
            self.assertEquals(len(list(results[id_])), 4)

    def test_get_steps_to_run(self):
        augmenter = self.get_data_augmenter()
        steps2run = augmenter._get_steps_to_run(exclude_all_but_step_type=SourceTargetSwapStep)
        self.assert_lists_have_the_same_vals(self.get_aug_ids(steps2run), [self.STEPS[0].get_aug_id()])

        steps2run = augmenter._get_steps_to_run(include_all_but_step_type=SourceTargetSwapStep)
        self.assert_lists_have_the_same_vals(self.get_aug_ids(steps2run), self.get_aug_ids(self.STEPS[1:]))

        steps2run = augmenter._get_steps_to_run()
        self.assert_lists_have_the_same_vals(self.get_aug_ids(steps2run), self.get_aug_ids(self.STEPS))

    def test_filter_step_type(self):
        filtered_steps = DataAugmenter._filter_step_type(steps=self.STEPS, step_type=SourceTargetSwapStep)
        self.assert_lists_have_the_same_vals(self.get_aug_ids(filtered_steps), self.get_aug_ids(self.STEPS[1:]))

    def test_get_step_type(self):
        step_of_type = DataAugmenter._get_step_of_type(steps=self.STEPS, step_type=SourceTargetSwapStep)
        self.assertEquals(step_of_type.get_aug_id(), self.STEPS[0].get_aug_id())

    def test_get_n_expected_for_step(self):
        n_expected = DataAugmenter._get_n_expected_for_step(self.STEPS[1], 10)
        self.assertEquals(5, n_expected)

    def get_aug_ids(self, steps):
        return [step.get_aug_id() for step in steps]

    def get_data_augmenter(self):
        return DataAugmenter(steps=self.STEPS)

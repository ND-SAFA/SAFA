from common_resources_test.base_tests.base_test import BaseTest
from common_resources.data.processing.augmentation.resample_step import ResampleStep


class TestResampleStep(BaseTest):
    RESAMPLE_RATE = 3

    def test_run(self):
        entry1 = ("source1", "target2")
        entry2 = ("source3", "target4")
        data_entries = [entry1, entry2]
        step = self.get_resample_step()

        augmented_data = list(step.run(data_entries))
        self.assertEqual(len(augmented_data), self.RESAMPLE_RATE * len(data_entries))
        self.resample_test(augmented_data, data_entries, self.RESAMPLE_RATE)

        n_expected = 9
        augmented_data_n_expected = list(step.run(data_entries, n_needed=n_expected))
        self.assertEqual(len(augmented_data_n_expected), n_expected)

    def test_augment(self):
        step = self.get_resample_step()
        resampled_entry = step._augment(("source", "target"))
        self.assertEqual(len(resampled_entry), 3)

    def get_resample_step(self):
        return ResampleStep(1, self.RESAMPLE_RATE)

    def resample_test(self, augmented_data, entries, resample_rate):
        entry1, entry2 = entries
        n_entries = [0, 0]
        for resampled_entry, reference_index in augmented_data:
            if resampled_entry == entry1:
                n_entries[0] += 1
                self.assertEqual(reference_index, 0)
            elif resampled_entry == entry2:
                n_entries[1] += 1
                self.assertEqual(reference_index, 1)
            else:
                self.fail("unknown entry " + resampled_entry)
        for n in n_entries:
            self.assertEqual(n, resample_rate)

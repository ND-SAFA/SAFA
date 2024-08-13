from tgen.testres.base_tests.base_test import BaseTest
from common_resources.data.processing.augmentation.source_target_swap_step import SourceTargetSwapStep


class TestSourceTargetSwapStep(BaseTest):

    def test_run(self):
        entry1 = ("source1", "target2")
        entry2 = ("source3", "target4")
        data_entries = [entry1, entry2]
        step = self.get_swap_step()
        augmented_data = list(step.run(data_entries, len(data_entries)))
        self.assertEqual(len(augmented_data), len(data_entries))
        n_entries = [0, 0]
        for resampled_entry, reference_index in augmented_data:
            if resampled_entry[0] == entry1[1]:
                n_entries[0] += 1
                self.assertEqual(reference_index, 0)
            elif resampled_entry[0] == entry2[1]:
                n_entries[1] += 1
                self.assertEqual(reference_index, 1)
            else:
                self.fail("unknown entry " + resampled_entry)
        for n in n_entries:
            self.assertEqual(n, 1)

    def test_augment(self):
        data_entry = ("source", "target")
        step = self.get_swap_step()
        swapped_entry = step._augment(data_entry)
        self.assertEqual(data_entry[1], swapped_entry[0])
        self.assertEqual(data_entry[0], swapped_entry[1])

    def get_swap_step(self):
        return SourceTargetSwapStep()

from test.base_test import BaseTest
from test.test_data import TEST_POS_LINKS, TEST_SOURCE_LAYERS, TEST_TARGET_LAYERS
from tracer.dataset import DatasetSplit


class TestTraceDataset(BaseTest):
    TEST_ENTRIES = [{"id": 1}, {"id": 2}, {"id": 3}, {"id": 4}, {"id": 5}, {"id": 6}]
    SOURCE_TARGET_PAIRS = [(s_id, t_id) for source_artifacts, target_artifacts in
                           zip(TEST_SOURCE_LAYERS, TEST_TARGET_LAYERS)
                           for s_id, t_id in zip(source_artifacts.keys(), target_artifacts.keys())]

    def test_resize_data_bigger(self):
        new_dataset = DatasetSplit._resize_data(TEST_POS_LINKS, 5)
        self.assertEquals(len(new_dataset), 5)

    def test_resize_data_duplicates(self):
        new_dataset = DatasetSplit._resize_data(TEST_POS_LINKS, 2, True)
        self.assertEquals(len(new_dataset), 2)

    def test_resize_data_size_smaller_no_duplicates(self):
        new_dataset = DatasetSplit._resize_data(TEST_POS_LINKS, 2, False)
        self.assertEquals(len(set(new_dataset)), 2)

    def test_resample_data(self):
        new_dataset = DatasetSplit._resample_data(TEST_POS_LINKS, 3)
        self.assertEquals(len(new_dataset), len(TEST_POS_LINKS) * 3)

    def test_add_entry(self):
        test_trace_dataset = self.get_test_trace_dataset()
        test_trace_dataset.add_entry(self.TEST_ENTRIES[0], self.SOURCE_TARGET_PAIRS[0])
        self.assertEquals(len(test_trace_dataset), 1)
        self.assertEquals(test_trace_dataset.data[0], self.TEST_ENTRIES[0])
        self.assertEquals(test_trace_dataset.source_target_pairs[0], self.SOURCE_TARGET_PAIRS[0])

    def test_add_entries(self):
        test_trace_dataset = self.get_test_trace_dataset()
        test_trace_dataset.add_entries(self.TEST_ENTRIES, self.SOURCE_TARGET_PAIRS)
        self.assertEquals(len(test_trace_dataset), len(self.TEST_ENTRIES))
        self.assertListEqual(test_trace_dataset.data, self.TEST_ENTRIES)
        self.assertListEqual(test_trace_dataset.source_target_pairs, self.SOURCE_TARGET_PAIRS)

    def get_test_trace_dataset(self):
        return DatasetSplit()

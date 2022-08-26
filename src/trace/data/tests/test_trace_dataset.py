from django.test import TestCase

from test.test_data import TEST_POS_LINKS, TEST_S_ARTS, TEST_T_ARTS
from trace.data.trace_dataset import TraceDataset


class TestTraceDataset(TestCase):
    TEST_ENTRIES = [{"id": 1}, {"id": 2}, {"id": 3}]
    SOURCE_TARGET_PAIRS = list(zip(TEST_S_ARTS.keys(), TEST_T_ARTS.keys()))

    def test_resize_data_bigger(self):
        new_dataset = TraceDataset.resize_data(TEST_POS_LINKS, 5)
        self.assertEquals(len(new_dataset), 5)

    def test_resize_data_duplicates(self):
        new_dataset = TraceDataset.resize_data(TEST_POS_LINKS, 2, True)
        self.assertEquals(len(new_dataset), 2)

    def test_resize_data_size_smaller_no_duplicates(self):
        new_dataset = TraceDataset.resize_data(TEST_POS_LINKS, 2, False)
        self.assertEquals(len(set(new_dataset)), 2)

    def test_resample_data(self):
        new_dataset = TraceDataset.resample_data(TEST_POS_LINKS, 3)
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
        return TraceDataset()

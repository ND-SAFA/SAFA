from data.datasets.splitting.supported_split_strategy import SupportedSplitStrategy
from data.datasets.splitting.trace_dataset_splitter import TraceDatasetSplitter
from testres.base_trace_test import BaseTraceTest
from testres.test_assertions import TestAssertions


class BaseSplitTest(BaseTraceTest):
    """
    Responsible for providing assertions for testing data split strategies.
    """

    def assert_split_multiple(self, strategy=SupportedSplitStrategy.SPLIT_BY_LINK):
        trace_dataset = self.get_trace_dataset()
        n_orig_links = len(trace_dataset)
        percent_splits = [0.3, 0.2]
        splitter = TraceDatasetSplitter(trace_dataset)
        splits = splitter.split_multiple(percent_splits, strategies=[strategy.name] * len(percent_splits))
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

    def assert_split(self, strategy=SupportedSplitStrategy.SPLIT_BY_LINK):
        trace_dataset = self.get_trace_dataset()
        splitter = TraceDatasetSplitter(trace_dataset)
        split1, split2 = splitter.split(self.VAlIDATION_PERCENTAGE, strategy=strategy.name)
        expected_val_link_size = (self.EXPECTED_VAL_SIZE_POS_LINKS + self.EXPECTED_VAL_SIZE_NEG_LINKS)
        self.assertLessEqual(abs(len(split1) - (len(self.all_links) - expected_val_link_size)), 1)
        self.assertLessEqual(abs(len(split2) - expected_val_link_size), 1)
        intersection = set(split1.links.keys()).intersection(set(split2.links.keys()))
        for t_id in intersection:
            print(trace_dataset.links[t_id])
        self.assertEquals(len(intersection), 0)

        for split in [split1, split2]:
            link_ids = split.pos_link_ids + split.neg_link_ids
            TestAssertions.assert_lists_have_the_same_vals(self, split.links.keys(), link_ids)

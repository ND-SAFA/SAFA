from collections import OrderedDict

from gen_common.data.tdatasets.dataset_role import DatasetRole
from gen_common.data.splitting.supported_split_strategy import SupportedSplitStrategy
from gen_common.data.splitting.dataset_splitter import DatasetSplitter
from gen_common_test.base_tests.base_trace_test import BaseTraceTest


class BaseSplitTest(BaseTraceTest):
    """
    Responsible for providing assertions for testing data split strategies.
    """

    def assert_split_multiple(self, strategy=SupportedSplitStrategy.SPLIT_BY_LINK):
        trace_dataset = self.get_trace_dataset()
        n_orig_links = len(trace_dataset)
        percent_splits = OrderedDict({DatasetRole.TRAIN: 0.5, DatasetRole.VAL: 0.3, DatasetRole.EVAL: 0.2})
        splitter = DatasetSplitter(trace_dataset, percent_splits, strategies=[strategy] * (len(percent_splits)-1))
        splits = splitter.split_dataset()
        split_link_ids = [set(split.trace_df.index) for split in splits.values()]
        self.assertEqual(sum([len(split) for split in splits.values()]), n_orig_links)
        for dataset_role, split in splits.items():
            self.assertLessEqual(abs(len(split) - round(n_orig_links * percent_splits[dataset_role])), 1)
        for i, split in enumerate(splits.values()):
            link_ids = split_link_ids[i]
            for j, other_link_ids in enumerate(split_link_ids):
                if i == j:
                    continue
                intersection = other_link_ids.intersection(link_ids)
                self.assertEqual(len(intersection), 0)
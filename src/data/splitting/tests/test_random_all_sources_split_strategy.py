from data.splitting.supported_split_strategy import SupportedSplitStrategy
from data.splitting.dataset_splitter import DatasetSplitter
from data.datasets.trace_dataset import TraceDataset
from testres.base_trace_test import BaseTraceTest


class TestRandomAllSourcesSplitStrategy(BaseTraceTest):
    SOURCES = {link.source.id for link in BaseTraceTest.all_links.values()}

    def test_one_of_each_source(self):
        trace_dataset = self.get_trace_dataset()
        splitter = DatasetSplitter(trace_dataset)
        split1, split2 = splitter.split(self.VAlIDATION_PERCENTAGE, strategy=SupportedSplitStrategy.ALL_SOURCES.name)
        split1: TraceDataset
        for source in self.SOURCES:
            self.assertIn(source, split1.trace_matrix.source_ids)

from data.datasets.trace_dataset import TraceDataset
from testres.base_test import BaseTest
from testres.test_data_manager import TestDataManager


class BaseTraceTest(BaseTest):
    VAlIDATION_PERCENTAGE = 0.3
    RESAMPLE_RATE = 3
    N_LINKS = len(TestDataManager.get_all_links())
    N_POSITIVE = len(TestDataManager.get_positive_links())
    N_NEGATIVE = len(TestDataManager.get_negative_links())
    EXPECTED_VAL_SIZE_NEG_LINKS = round((N_LINKS - N_POSITIVE) * VAlIDATION_PERCENTAGE)
    EXPECTED_VAL_SIZE_POS_LINKS = round(N_POSITIVE * VAlIDATION_PERCENTAGE)
    positive_links = TestDataManager._create_link_map(TestDataManager.get_positive_links())
    all_links = TestDataManager._create_link_map(TestDataManager.get_all_links())
    negative_links = TestDataManager._create_link_map(TestDataManager.get_negative_links())

    @staticmethod
    def get_trace_dataset():
        links = TestDataManager._create_link_map(TestDataManager.get_all_links())
        pos_links_ids = TestDataManager.get_positive_link_ids()
        for link in links.values():
            if link.id in pos_links_ids:
                link.is_true_link = True
        return TraceDataset(links, pos_link_ids=TestDataManager.get_positive_link_ids(),
                            neg_link_ids=TestDataManager.get_negative_link_ids())

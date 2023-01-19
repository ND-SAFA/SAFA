from data.datasets.trace_dataset import TraceDataset
from testres.base_test import BaseTest
from testres.test_data_manager import TestDataManager
from testres.testprojects.api_test_project import ApiTestProject


class BaseTraceTest(BaseTest):
    VAlIDATION_PERCENTAGE = 0.3
    RESAMPLE_RATE = 3
    N_LINKS = len(ApiTestProject.get_expected_links())
    N_POSITIVE = len(ApiTestProject.get_positive_links())
    N_NEGATIVE = len(ApiTestProject.get_negative_links())
    EXPECTED_VAL_SIZE_NEG_LINKS = round((N_LINKS - N_POSITIVE) * VAlIDATION_PERCENTAGE)
    EXPECTED_VAL_SIZE_POS_LINKS = round(N_POSITIVE * VAlIDATION_PERCENTAGE)
    positive_links = TestDataManager.create_link_map(ApiTestProject.get_positive_links())
    all_links = TestDataManager.create_link_map(ApiTestProject.get_expected_links())
    negative_links = TestDataManager.create_link_map(ApiTestProject.get_negative_links())

    @staticmethod
    def get_trace_dataset():
        links = TestDataManager.create_link_map(ApiTestProject.get_expected_links())
        pos_links_ids = ApiTestProject.get_positive_link_ids()
        negative_link_ids = []
        for link in links.values():
            if link.id in pos_links_ids:
                link.is_true_link = True
            else:
                negative_link_ids.append(link.id)
        return TraceDataset(links, pos_link_ids=pos_links_ids, neg_link_ids=negative_link_ids)

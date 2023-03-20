from data.dataframes.layer_dataframe import LayerDataFrame
from data.dataframes.trace_dataframe import TraceKeys
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
    positive_links = TestDataManager.create_trace_dataframe(ApiTestProject.get_positive_links())
    all_links = TestDataManager.create_trace_dataframe(ApiTestProject.get_expected_links())
    negative_links = TestDataManager.create_trace_dataframe(ApiTestProject.get_negative_links())

    @staticmethod
    def get_trace_dataset():
        trace_df = TestDataManager.create_trace_dataframe(ApiTestProject.get_expected_links())
        artifacts_df = TestDataManager.create_artifact_dataframe()
        pos_links_ids = ApiTestProject.get_positive_link_ids()
        negative_link_ids = []
        for index in trace_df.index:
            if index in pos_links_ids:
                trace_df.at[index, TraceKeys.LABEL.value] = 1
            else:
                negative_link_ids.append(index)
        return TraceDataset(artifact_df=artifacts_df, trace_df=trace_df, layer_mapping_df=LayerDataFrame())

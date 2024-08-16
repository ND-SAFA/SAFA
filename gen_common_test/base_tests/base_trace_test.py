from gen_common.data.dataframes.layer_dataframe import LayerDataFrame
from gen_common.data.keys.structure_keys import TraceKeys, LayerKeys
from gen_common.data.tdatasets.trace_dataset import TraceDataset
from gen_common_test.base_tests.base_test import BaseTest
from gen_common_test.test_data.test_data_manager import TestDataManager
from gen_common_test.testprojects.api_test_project import ApiTestProject


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
        artifact_df = TestDataManager.create_artifact_dataframe()
        pos_links_ids = ApiTestProject.get_positive_link_ids()
        negative_link_ids = []
        for index in trace_df.index:
            if index in pos_links_ids:
                trace_df.at[index, TraceKeys.LABEL.value] = 1
            else:
                negative_link_ids.append(index)
        return TraceDataset(artifact_df=artifact_df, trace_df=trace_df,
                            layer_df=LayerDataFrame({LayerKeys.SOURCE_TYPE: ["source_1", "source_2"],
                                                     LayerKeys.TARGET_TYPE: ["target_1", "target_2"]}))

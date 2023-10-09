from tgen.common.util.enum_util import EnumDict
from tgen.data.dataframes.trace_dataframe import TraceDataFrame
from tgen.data.keys.structure_keys import TraceKeys
from tgen.testres.base_tests.base_test import BaseTest


class TestTraceDataFrame(BaseTest):

    def test_add_link(self):
        df = self.get_trace_data_frame()
        link = df.add_link(source_id="s3", target_id="t3", label=1)
        self.assert_link(link, "s3", "t3", 1, TraceDataFrame.generate_link_id("s3", "t3"))

        df_empty = TraceDataFrame()
        link = df_empty.add_link(source_id="s3", target_id="t3", label=1)
        self.assert_link(link, "s3", "t3", 1, TraceDataFrame.generate_link_id("s3", "t3"))

    def test_get_link(self):
        df = self.get_trace_data_frame()
        link = df.get_link(source_id="s2", target_id="t2")
        self.assert_link(link, "s2", "t2", 1, TraceDataFrame.generate_link_id("s2", "t2"))

        link_does_not_exist = df.get_link(source_id="s3", target_id="t3")
        self.assertIsNone(link_does_not_exist)

    def test_to_dict(self):
        df = TraceDataFrame(EnumDict({TraceKeys.SOURCE: ["s1", "s1"], TraceKeys.TARGET: ["t1", "t1"],
                                      TraceKeys.LABEL: [0, 1]}))
        without_dups = df.to_dict(orient="index")
        self.assertSize(1, without_dups)

    def assert_link(self, link: EnumDict, source_id, target_id, label, link_id):
        self.assertEqual(link[TraceKeys.SOURCE], source_id)
        self.assertEqual(link[TraceKeys.TARGET], target_id)
        self.assertEqual(link[TraceKeys.LABEL], label)
        self.assertEqual(link[TraceKeys.LINK_ID], link_id)

    def get_trace_data_frame(self):
        return TraceDataFrame(EnumDict({TraceKeys.SOURCE: ["s1", "s2"], TraceKeys.TARGET: ["t1", "t2"],
                                        TraceKeys.LABEL: [0, 1]}))

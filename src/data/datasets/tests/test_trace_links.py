from data.tree.trace_dataframe import TraceDataFrame
from testres.base_test import BaseTest


class TestTraceLinks(BaseTest):

    def test_assert_columns(self):
        df1 = TraceDataFrame()
        link = df1.add_link(source_id=1, target_id=2)
        link
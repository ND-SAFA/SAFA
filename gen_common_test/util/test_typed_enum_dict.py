from gen_common.data.objects.trace import Trace
from gen_common.data.keys.structure_keys import TraceKeys
from gen_common_test.base_tests.base_test import BaseTest


class TestTypedEnumDict(BaseTest):

    def test_trace(self):
        trace = Trace(link_id=1, source="source", target="target", score=0.5, label=1, explanation="explanation")
        source = trace.get(TraceKeys.SOURCE)
        self.assertEqual(source, "source")

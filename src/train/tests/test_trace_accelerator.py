from testres.base_trace_test import BaseTraceTest
from train.trace_accelerator import TraceAccelerator


class TestTraceAccelerator(BaseTraceTest):

    def test_get_attr(self):
        TraceAccelerator.is_local_main_process

from test.base_test import BaseTest
from trace.data.data_objects.artifact import Artifact
from trace.data.data_objects.trace_link import TraceLink

FEATURE_VALUE = "({}, {})"


def fake_method(text, text_pair, return_token_type_ids, add_special_tokens):
    return {"feature_name": FEATURE_VALUE.format(text, text_pair)}


class TestTraceLink(BaseTest):
    S_ID = "sid"
    T_ID = "tid"
    S_TOKEN = "s_token"
    T_TOKEN = "t_token"

    def test_get_feature(self):
        expected_value = FEATURE_VALUE.format(self.S_TOKEN, self.T_TOKEN)
        test_trace_link = self.get_test_trace_link()
        feature = test_trace_link.get_feature()
        self.assertEquals(feature["feature_name"], expected_value)

        # second time calling get_feature should not call feature_func again
        test_trace_link.token = "changed_token"
        feature = test_trace_link.get_feature()
        self.assertEquals(feature["feature_name"], expected_value)

    def test_get_source_target_ids(self):
        link = self.get_test_trace_link()
        source_target_ids = link.get_source_target_ids()
        self.assertEqual(source_target_ids, (self.S_ID, self.T_ID))

    def test_generate_link_id(self):
        link_id = TraceLink.generate_link_id(self.S_ID, self.T_ID)
        self.assertEquals(link_id - hash(self.S_ID), hash(self.T_ID))
        self.assertEquals(link_id - hash(self.T_ID), hash(self.S_ID))

    def get_test_trace_link(self):
        source = Artifact(self.S_ID, self.S_TOKEN, lambda text: text)
        target = Artifact(self.T_ID, self.T_TOKEN, lambda text: text)
        return TraceLink(source, target, fake_method)

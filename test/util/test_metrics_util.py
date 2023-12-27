from tgen.common.util.metrics_util import MetricsUtil
from tgen.testres.base_tests.base_test import BaseTest


class TestMetricsUtil(BaseTest):

    def test_has_labels(self):
        self.assertFalse(MetricsUtil.has_labels([0, 1, 0.5, 1, 0.8, 0, 0.2]))
        self.assertTrue(MetricsUtil.has_labels([0, 1, 1, 0]))
import mock
from mock import patch

from tgen.metrics.supported_trace_metric import get_metric_path
from tgen.testres.base_tests.base_test import BaseTest


class TestSupportedTraceMetric(BaseTest):
    TEST_LIST_METRICS = ["accuracy"]

    def test_get_metric_path(self):
        path = get_metric_path("MAP")
        self.assertIn("metrics/map_metric.py", path)

    @patch("datasets.list_metrics")
    def test_get_metric_path_unknown(self, list_metrics_mock: mock.MagicMock):
        list_metrics_mock.return_value = self.TEST_LIST_METRICS
        self.assertRaises(NameError, lambda: get_metric_path("unknown_metric"))

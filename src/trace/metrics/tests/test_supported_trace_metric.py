import mock
from mock import patch

from test.base_test import BaseTest
from trace.metrics.supported_trace_metric import get_metric_path


class TestSupportedTraceMetric(BaseTest):
    TEST_LIST_METRICS = ["accuracy"]

    def test_get_metric_path(self):
        path = get_metric_path("map_at_k")
        self.assertIn("src/trace/metrics/map_at_k_metric.py", path)

    @patch("models.list_metrics")
    def test_get_metric_path_from_datasets(self, list_metrics_mock: mock.MagicMock):
        list_metrics_mock.return_value = self.TEST_LIST_METRICS
        path = get_metric_path("accuracy")
        self.assertEquals(path, "accuracy")

    @patch("models.list_metrics")
    def test_get_metric_path_unknown(self, list_metrics_mock: mock.MagicMock):
        list_metrics_mock.return_value = self.TEST_LIST_METRICS
        self.assertRaises(NameError, lambda: get_metric_path("unknown_metric"))

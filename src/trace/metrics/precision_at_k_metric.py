from train.metrics.trace_metric import TraceMetric
from constants import K_METRIC_DEFAULT


class PrecisionAtKMetric(TraceMetric):

    @property
    def name(self) -> str:
        return "precision_at_k"

    # TODO
    def _perform_compute(self, predictions, labels, k=K_METRIC_DEFAULT, **kwargs) -> float:
        pass

    def _info(self):
        # TODO: Specifies the datasets.MetricInfo object
        pass

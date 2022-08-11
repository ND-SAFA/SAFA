from trace.metrics.trace_metric import TraceMetric


class MRRMetric(TraceMetric):

    @property
    def name(self) -> str:
        return "mrr"

    # TODO
    def _perform_compute(self, predictions, labels, **kwargs) -> float:
        pass

    def _info(self):
        # TODO: Specifies the datasets.MetricInfo object
        pass

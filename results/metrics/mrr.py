from results.metrics.lmmetric import LMMetric


class MRR(LMMetric):

    @property
    def name(self) -> str:
        return "mrr"

    # TODO
    def _perform_compute(self, predictions, labels, **kwargs) -> float:
        pass

    def _info(self):
        # TODO: Specifies the datasets.MetricInfo object
        pass

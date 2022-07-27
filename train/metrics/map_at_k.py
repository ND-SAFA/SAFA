from train.metrics.lmmetric import LMMetric
from constants import K_METRIC_DEFAULT


class MAPatK(LMMetric):

    @property
    def name(self) -> str:
        return "map_at_k"

    # TODO
    def _perform_compute(self, predictions, labels, k=K_METRIC_DEFAULT, **kwargs) -> float:
        pass

    def _info(self):
        # TODO: Specifies the datasets.MetricInfo object
        pass

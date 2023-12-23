from typing import List


class MetricsUtil:

    @staticmethod
    def has_labels(predictions: List[float]) -> bool:
        """
        Returns True if the predictions have labels (0, 1) or False if they are scores [0, 1].
        :param predictions: List of predictions.
        :return: True if the predictions have labels (0, 1) or False if they are scores [0, 1].
        """
        return all(p == 0 or p == 1 for p in predictions)

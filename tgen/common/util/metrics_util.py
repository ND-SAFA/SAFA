from typing import List


class MetricsUtil:

    @staticmethod
    def has_labels(predictions: List[float]) -> bool:
        """
        Returns True if the predictions have labels (e.g. 0, 1, discrete values...) or False if they are scores (continuous value).
        :param predictions: List of predictions.
        :return: True if the predictions have labels (e.g. 0, 1, discrete values...) or False if they are scores (continuous value).
        """
        return all(round(p) == p for p in predictions)

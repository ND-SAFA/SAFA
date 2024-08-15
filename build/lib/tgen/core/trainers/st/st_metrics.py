from typing import Dict, List, TypedDict


class STMetrics(TypedDict):
    """
    :param records: The metric records for each evaluation. Each record is a map of the dataset role to the metrics.
    :param losses: The list of losses per training step.
    """
    records: List[Dict]
    losses: List[float]

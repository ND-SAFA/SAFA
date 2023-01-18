from typing import Dict, List, Tuple, TypedDict


class ApiDefinition(TypedDict):
    """
    Defines the API payload for training or predicting on a model.
    Note, `links` not included during prediction.
    """
    source_layers: List[Dict[str, str]]
    target_layers: List[Dict[str, str]]
    true_links: List[Tuple[str, str]]

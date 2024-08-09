from typing import List

from common_resources.data.keys.structure_keys import TraceKeys
from common_resources.data.objects.trace import Trace


class RankingUtil:

    @staticmethod
    def group_trace_predictions(predictions: List[Trace], key_id: str, sort_entries: bool = False):
        """
        Groups the predictions by the property given.
        :param predictions: The predictions to group.
        :param key_id: The id of the key to access the child from the entry
        :param sort_entries: If True, sorts all predictions for each grouping.
        :return: Dictionary of keys in key_id and their associated entries.
        """
        artifact_id2entries = {}
        for entry in predictions:
            a_id = entry[key_id]
            if a_id not in artifact_id2entries:
                artifact_id2entries[a_id] = []
            artifact_id2entries[a_id].append(entry)
        if sort_entries:
            artifact_id2entries = {a_id: sorted(entries, key=lambda entry: entry[TraceKeys.SCORE], reverse=True)
                                   for a_id, entries in artifact_id2entries.items()}
        return artifact_id2entries

import random
from typing import Callable

from tgen.ranking.pipeline.base import RankingStore, get_trace_id
from tgen.util.json_util import JsonUtil


def store_predictions(s: RankingStore, entries, on_entry: Callable = None):
    traced_ids = []
    target_ids = set()

    for entry in entries:
        if entry["label"] == 1:
            traced_ids.append(get_trace_id(entry))
        if on_entry:
            on_entry(entry)
        target_ids.add(entry["target"])
    s.traced_ids = traced_ids
    s.all_target_ids = list(target_ids)


def read_positive_predictions(s: RankingStore):
    prediction_entries = JsonUtil.read_json_file(s.run_path)["body"]["prediction_entries"]
    positive_entries = []

    def on_entry(entry):
        if entry["score"] >= 0.5:
            positive_entries.append(entry)

    random.shuffle(prediction_entries)
    store_predictions(s, prediction_entries, on_entry)
    s.trace_entries = positive_entries

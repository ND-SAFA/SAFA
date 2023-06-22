from typing import Callable

from paper.pipeline.base import RankingStore, get_trace_id
from tgen.data.creators.trace_dataset_creator import TraceDatasetCreator
from tgen.data.readers.structured_project_reader import StructuredProjectReader
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
    s.target_ids = list(target_ids)


def read_labels(s: RankingStore):
    project_reader = StructuredProjectReader(s.project_path)
    trace_dataset_creator = TraceDatasetCreator(project_reader)
    trace_dataset = trace_dataset_creator.create()

    entries = []
    for i, row in trace_dataset.trace_df.iterrows():
        entry = {
            "source": row["source"],
            "target": row["target"],
            "label": row["label"]
        }
        entries.append(entry)
    s.trace_entries = entries
    store_predictions(s, entries)


def read_positive_predictions(s: RankingStore):
    dataset_path = s.run_path
    prediction_entries = JsonUtil.read_json_file(s.run_path)["body"]["prediction_entries"]
    positive_entries = []

    def on_entry(entry):
        if entry["score"] >= 0.5:
            positive_entries.append(entry)

    store_predictions(s, prediction_entries, on_entry)
    s.trace_entries = positive_entries

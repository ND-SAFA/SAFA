import os
from dataclasses import dataclass

import pandas as pd

from tgen.data.dataframes.trace_dataframe import TraceDataFrame, TraceKeys
from tgen.train.save_strategy.abstract_save_strategy import SupportedComparisonFunction
from tgen.util.json_util import JsonUtil


@dataclass
class TraceLinkFilter:
    """
    Applies a filter to a trace link dataset.
    """
    rq_path: str
    comparison_function: SupportedComparisonFunction
    threshold: float = 0.5

    def filter(self, trace_df: TraceDataFrame) -> TraceDataFrame:
        output_path = os.path.join(self.rq_path, "output.json")
        rq_json = JsonUtil.read_json_file(output_path)
        prediction_entries = rq_json["body"]["prediction_entries"]
        if isinstance(self.comparison_function, str):
            self.comparison_function = SupportedComparisonFunction[self.comparison_function]
        entries_accepted = {}
        for entry in prediction_entries:
            if self.comparison_function.value(entry["score"], self.threshold):
                source_name = entry["source"]
                target_name = entry["target"]
                if source_name not in entries_accepted:
                    entries_accepted[source_name] = set()
                entries_accepted[source_name].add(target_name)

        def row_filter(row: pd.Series) -> bool:
            return row[TraceKeys.SOURCE.value] not in entries_accepted or row[TraceKeys.TARGET.value] not in entries_accepted[
                row[TraceKeys.SOURCE.value]]

        filtered_trace_df = trace_df.filter_by_row(row_filter)
        return filtered_trace_df

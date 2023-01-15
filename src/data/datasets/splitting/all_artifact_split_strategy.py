from typing import List

from config.override import overrides
from data.datasets.splitting.abstract_split_strategy import AbstractSplitStrategy
from data.datasets.trace_dataset import TraceDataset
from data.tree.trace_link import TraceLink


class AllArtifactSplitStrategy(AbstractSplitStrategy):
    """
    Responsible for splitting a dataset randomly while ensuring each source and target appears once in training.
    """

    @staticmethod
    @overrides(AbstractSplitStrategy)
    def create_split(trace_dataset: TraceDataset, percent_split: float, slice_num: int) -> "TraceDataset":
        """
        Creates a new trace data from the slice defined by the percent split referencing all artifacts in trace dataset.
        :param trace_dataset: The trace dataset to split.
        :param percent_split: The percentage of links included in second slice.
        :param slice_num: Whether to return first or second slice.
        :return: the dataset split
        """

        sources_seen = []
        targets_seen = []
        first_split_links = []
        links: List[TraceLink] = list(trace_dataset.links.values())

        for source_id in trace_dataset.trace_matrix.source_ids:  # will select one link per source
            source_traces = trace_dataset.trace_matrix.query_matrix[source_id]
            source_traces = source_traces.links.copy()
            for source_trace in source_traces:  # select link containing new target
                source_id = source_trace.source.id
                target_id = source_trace.target.id
                if target_id not in targets_seen:
                    targets_seen.append(target_id)
                    sources_seen.append(source_id)
                    first_split_links.append(source_trace.id)
                    break

        for link in links:  # ensures all targets are covered
            if link.target.id not in targets_seen:
                first_split_links.append(link.id)
                targets_seen.append(link.target.id)

        if percent_split * len(links) < len(first_split_links):
            raise ValueError(f"Referencing all artifacts led to split greater than percentage desired: {percent_split}.")
        return AbstractSplitStrategy.create_split_containing_specified_link_ids(trace_dataset=trace_dataset,
                                                                                link_ids_for_first_split=first_split_links,
                                                                                percent_split=percent_split,
                                                                                slice_num=slice_num)

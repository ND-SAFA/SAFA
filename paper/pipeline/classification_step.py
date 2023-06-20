from paper.pipeline.base import RankingStore


def add_precision(s: RankingStore):
    n = 3
    metrics = {}
    for instructions in s.map_instructions:
        total_links = instructions["total"]
        positive_indices = instructions["indices"]

        for i in range(1, n + 1):
            tp_indices = list(filter(lambda pos_index: pos_index + 1 <= i, positive_indices))
            tp = len(tp_indices)
            fp = i - tp
            precision = tp / (tp + fp)
            metrics[f"Precision@{i}"] = precision
    s.metrics["base"].update(metrics)

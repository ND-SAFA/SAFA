from tgen.ranking.pipeline.base import RankingStore


def compute_precision(s: RankingStore):
    metrics = s.metrics["base"]
    add_precision_to_metrics(metrics, s.map_instructions)


def add_precision_to_metrics(metrics, map_instructions, n=3):
    for instructions in map_instructions:
        total_links = instructions["total"]
        positive_indices = instructions["indices"]

        for i in range(1, n + 1):
            tp_indices = list(filter(lambda pos_index: pos_index + 1 <= i, positive_indices))
            tp = len(tp_indices)
            fp = i - tp
            precision = tp / (tp + fp)
            metrics[f"Precision@{i}"] = precision

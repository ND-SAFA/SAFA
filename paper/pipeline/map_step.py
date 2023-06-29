from typing import Dict, List

import numpy as np
from sklearn.metrics import average_precision_score

from paper.pipeline.base import RankingStore, get_trace_id


def compute_map(s: RankingStore):
    source_ids = s.source_ids
    map_instructions = s.map_instructions
    s.metrics = {}
    metrics = calculate_map(s.metrics, map_instructions, source_ids)


def calculate_map(metrics: Dict, map_instructions: List[Dict], source_ids: List[str]) -> Dict:
    def create_increment_list(n_items):
        increment = 1 / (n_items - 1)  # Calculate the linear increment
        return [1 - (i * increment) for i in range(n_items)]  # Generate the list

    def create_label_list(label_indices):
        l_list = [0] * n_items
        for pos_index in label_indices:
            l_list[pos_index] = 1
        return l_list

    ap_scores = []
    for s_name, instructions in zip(source_ids, map_instructions):
        n_items = instructions["total"]
        positive_indices = instructions["indices"]
        labels = create_label_list(positive_indices)

        # Predictions
        predictions = create_increment_list(n_items)
        predictions = predictions[:n_items]

        ap_score = average_precision_score(labels, predictions)
        ap_score = ap_score if not np.isnan(ap_score) else 0
        metrics[s_name] = {"ap": ap_score}
        ap_scores.append(ap_score)
    map_score = sum(ap_scores) / len(ap_scores)
    metrics["base"] = {"map": map_score}
    return metrics


def create_metric_instructions(s: RankingStore):
    traced_ids = s.traced_ids
    source_ids = s.source_ids
    ranked_target_links = s.processed_ranking_response

    map_instructions = calculate_map_instructions(ranked_target_links, source_ids, traced_ids)
    s.map_instructions = map_instructions


def calculate_map_instructions(predicted_target_links, source_ids, traced_ids):
    map_instructions: List[Dict] = []
    for s_id, target_ranked_list in zip(source_ids, predicted_target_links):
        s_pos_indices = []
        for i, t_id in enumerate(target_ranked_list):
            trace_id = get_trace_id({"source": s_id, "target": t_id})
            if trace_id in traced_ids:
                s_pos_indices.append(i)
        map_instructions.append({
            "total": len(target_ranked_list),
            "indices": s_pos_indices
        })
    return map_instructions

import random
from typing import Dict, List

from sklearn.metrics import average_precision_score

from paper.pipeline.base import RankingStore, get_trace_id, remove_file_extension


def compute_map(s: RankingStore):
    source_ids = s.source_ids
    map_instructions = s.map_instructions
    metrics = {}

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
        metrics[s_name] = {"ap": ap_score}
        ap_scores.append(ap_score)
    map_score = sum(ap_scores) / len(ap_scores)
    metrics["base"] = {"map": map_score}
    s.metrics = metrics


response_processing_steps = [lambda s: s.replace("ID:", ""), lambda s: s.split(",")]
id_processing_steps = [remove_file_extension, lambda f: f.replace("ID:", ""), lambda f: f.strip()]


def process_response(orig):
    processed = orig
    for s in response_processing_steps:
        processed = s(processed)
    return processed


def process_artifact_ids(raw_artifact_ids):
    response = []
    for raw_artifact_id in raw_artifact_ids:
        processed = raw_artifact_id
        for s in id_processing_steps:
            processed = s(processed)
        response.append(processed)
    return response


def create_map_instructions(s: RankingStore):
    traced_ids = s.traced_ids
    source_ids = s.source_ids
    ranked_target_links: List[List[str]] = process_ranked_artifacts(s.batch_response, s.target_ids)

    map_instructions: List[Dict] = []
    for s_id, target_ranked_list in zip(source_ids, ranked_target_links):
        s_pos_indices = []
        for i, t_id in enumerate(target_ranked_list):
            trace_id = get_trace_id({"source": s_id, "target": t_id})
            if trace_id in traced_ids:
                s_pos_indices.append(i)
        map_instructions.append({
            "total": len(target_ranked_list),
            "indices": s_pos_indices
        })
    s.ranked_predictions = ranked_target_links
    s.map_instructions = map_instructions


def process_ranked_artifacts(batch_response, target_ids, add_missing=True) -> List[List[str]]:
    target_ids = list(map(lambda f: remove_file_extension(f), target_ids))
    ranked_target_links = []
    for response in batch_response.batch_responses:
        processed_response = process_response(response)
        processed_artifact_ids = process_artifact_ids(processed_response)
        ranked_target_links.append(processed_artifact_ids)
    if add_missing:
        for r_list in ranked_target_links:
            missing_ids = [t_id for t_id in target_ids if t_id not in r_list]
            random.shuffle(missing_ids)
            r_list.extend(missing_ids)
    return ranked_target_links

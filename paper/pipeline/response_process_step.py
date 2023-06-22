import random
from typing import List

from paper.pipeline.base import RankingStore, remove_file_extension

RESPONSE_PROCESSING_STEPS = [lambda s: s.replace("ID:", ""), lambda s: s.split(",")]
ID_PROCESSING_STEPS = [remove_file_extension, lambda f: f.replace("ID:", ""), lambda f: f.strip()]


def process_ranking_prompts(s: RankingStore):
    s.processed_response: List[List[str]] = process_ranked_artifacts(s.batch_response, s.target_ids)


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


def process_artifact_ids(raw_artifact_ids):
    response = []
    for raw_artifact_id in raw_artifact_ids:
        processed = raw_artifact_id
        for s in ID_PROCESSING_STEPS:
            processed = s(processed)
        response.append(processed)
    return response


def process_response(orig):
    processed = orig
    for s in RESPONSE_PROCESSING_STEPS:
        processed = s(processed)
    return processed

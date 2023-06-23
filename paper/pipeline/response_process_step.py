import random
from typing import List

from paper.pipeline.base import RankingStore
from tgen.util.llm_response_util import LLMResponseUtil

RESPONSE_PROCESSING_STEPS = [
    lambda r: LLMResponseUtil.parse(r, "links"),
    lambda s: s.replace("ID:", ""),
    lambda s: s.split(",")
]
ID_PROCESSING_STEPS = [lambda f: f.replace("ID:", ""), lambda f: f.strip()]


def process_ranking_prompts(s: RankingStore):
    s.processed_response: List[List[str]] = process_ranked_artifacts(s)


def process_ranked_artifacts(s: RankingStore, add_missing=True) -> List[List[str]]:
    batch_response = s.batch_response
    target_ids = s.all_target_ids

    ranked_target_links = []
    for response, source_name in zip(batch_response.batch_responses, s.source_ids):
        processed_response = process_response(response)  # string response into list
        processed_artifact_ids = process_artifact_ids(processed_response)  # processes each artifact id
        related_targets = s.source2targets[source_name]
        translated_artifact_ids = translate_indices(processed_artifact_ids, related_targets)
        ranked_target_links.append(translated_artifact_ids)
    if add_missing:
        for r_list in ranked_target_links:
            missing_ids = [t_id for t_id in target_ids if t_id not in r_list]
            random.shuffle(missing_ids)
            r_list.extend(missing_ids)
    return ranked_target_links


def translate_indices(processed_artifact_ids: List[str], related_targets):
    processed_artifact_ids = list(map(lambda i: int(i), processed_artifact_ids))
    processed_artifact_ids = list(filter(lambda i: i < len(related_targets), processed_artifact_ids))
    processed_artifact_ids = list(map(lambda i: related_targets[i], processed_artifact_ids))
    return processed_artifact_ids


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

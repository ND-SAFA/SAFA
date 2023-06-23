import random
from typing import List

from paper.common.completion_util import complete_prompts
from paper.common.ranking_prompt_builder import RankingPromptBuilder
from paper.pipeline.base import RankingStore
from paper.pipeline.ipipeline import iPipeline
from tgen.util.llm_response_util import LLMResponseUtil

RESPONSE_PROCESSING_STEPS = [
    lambda r: LLMResponseUtil.parse(r, "links"),
    lambda s: s.replace("ID:", ""),
    lambda s: s.split(",")
]
ID_PROCESSING_STEPS = [lambda f: f.replace("ID:", ""), lambda f: f.strip()]


class RankingStep(iPipeline):
    def __init__(self):
        steps = [self.create_ranking_prompts, self.complete_ranking_prompts, self.process_ranking_prompts]
        super().__init__(steps)

    @staticmethod
    def create_ranking_prompts(s: RankingStore):
        artifact_map = s.artifact_map
        source_names = s.source_ids

        prompts = []
        for s_name in source_names:
            prompt = RankingStep.create_prompts(artifact_map, s_name, s)
            prompts.append(prompt)

        s.ranking_prompts = prompts

    @staticmethod
    def create_prompts(artifact_map, source_name, s: RankingStore):
        target_names = s.source2targets[source_name]
        source_body = artifact_map[source_name]
        prompt_builder = RankingPromptBuilder(goal=s.ranking_goal,
                                              instructions=s.ranking_instructions,
                                              query=source_body,
                                              body_title="# Artifacts")
        for target_index, target_artifact_name in enumerate(target_names):
            prompt_builder.with_artifact(target_index, artifact_map[target_artifact_name])
        if source_name in s.source2reason:
            prompt_builder.with_context(s.source2reason[source_name])
        prompt = prompt_builder.get()
        return prompt

    @staticmethod
    def complete_ranking_prompts(s: RankingStore):
        batch_response = complete_prompts(s.ranking_prompts, max_tokens=2000)
        s.ranking_responses = batch_response

    @staticmethod
    def process_ranking_prompts(s: RankingStore):
        s.processed_ranking_response: List[List[str]] = RankingStep.process_ranked_artifacts(s)

    @staticmethod
    def process_ranked_artifacts(s: RankingStore, add_missing=True) -> List[List[str]]:
        batch_response = s.ranking_responses
        target_ids = s.all_target_ids

        ranked_target_links = [[] for _ in range(len(s.source_ids))]
        for source_name, prompt_response in zip(s.source_ids, batch_response.batch_responses):
            source_index = s.source_ids.index(source_name)
            related_targets = s.source2targets[source_name]

            response_list = RankingStep.convert_response_to_list(prompt_response)  # string response into list
            artifact_indices = RankingStep.parse_artifact_indices(response_list)  # processes each artifact id
            artifact_ids = RankingStep.translate_indices_to_ids(artifact_indices, related_targets)
            ranked_target_links[source_index].extend(artifact_ids)

        if add_missing:
            for r_list in ranked_target_links:
                missing_ids = [t_id for t_id in target_ids if t_id not in r_list]
                random.shuffle(missing_ids)
                r_list.extend(missing_ids)
        return ranked_target_links

    @staticmethod
    def translate_indices_to_ids(processed_artifact_ids: List[str], related_targets):
        processed_artifact_ids = list(map(lambda i: int(i), processed_artifact_ids))
        processed_artifact_ids = list(filter(lambda i: i < len(related_targets), processed_artifact_ids))
        processed_artifact_ids = list(map(lambda i: related_targets[i], processed_artifact_ids))
        return processed_artifact_ids

    @staticmethod
    def parse_artifact_indices(raw_artifact_ids):
        response = []
        for raw_artifact_id in raw_artifact_ids:
            processed = raw_artifact_id
            for s in ID_PROCESSING_STEPS:
                processed = s(processed)
            response.append(processed)
        return response

    @staticmethod
    def convert_response_to_list(orig):
        processed = orig
        for s in RESPONSE_PROCESSING_STEPS:
            processed = s(processed)
        return processed

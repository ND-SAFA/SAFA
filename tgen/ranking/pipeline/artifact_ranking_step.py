import random
from typing import Dict, List

from tgen.ranking.common.completion_util import complete_prompts
from tgen.ranking.common.ranking_prompt_builder import RankingPromptBuilder
from tgen.ranking.pipeline.base import RankingStore
from tgen.ranking.pipeline.ipipeline import iPipeline
from tgen.util.llm_response_util import LLMResponseUtil

RESPONSE_PROCESSING_STEPS = [
    lambda r: LLMResponseUtil.parse(r, "links"),
    lambda s: s.replace("ID:", ""),
    lambda s: s.split(",")
]
ID_PROCESSING_STEPS = [lambda f: f.replace("ID:", ""), lambda f: f.strip()]


class ArtifactRankingStep(iPipeline):
    def __init__(self):
        """
        Ranks children artifacts from most to least related to source.
        """
        steps = [self.create_ranking_prompts, self.complete_ranking_prompts, self.process_ranking_prompts]
        super().__init__(steps)

    @staticmethod
    def create_ranking_prompts(s: RankingStore) -> None:
        """
        Creates the prompts to rank children.
        :param s: The ranking store.
        :return: None
        """
        artifact_map = s.artifact_map
        parent_names = s.parent_ids

        prompts = []
        for p_name in parent_names:
            prompt = ArtifactRankingStep.create_prompts(artifact_map, p_name, s)
            prompts.append(prompt)

        s.ranking_prompts = prompts

    @staticmethod
    def create_prompts(artifact_map: Dict[str, str], parent_id: str, s: RankingStore) -> str:
        """
        Creates ranking prompt for parent artifact.
        :param artifact_map: Map of artifact id to body.
        :param parent_id: The id of the parent to create prompt for.
        :param s: The ranking store.
        :return: The ranking prompt.
        """
        target_names = s.parent2children[parent_id]
        source_body = artifact_map[parent_id]
        prompt_builder = RankingPromptBuilder(goal=s.ranking_goal,
                                              instructions=s.ranking_instructions,
                                              query=source_body,
                                              body_title="# Artifacts")
        for target_index, target_artifact_name in enumerate(target_names):
            prompt_builder.with_artifact(target_index, artifact_map[target_artifact_name])
        if parent_id in s.source2reason:
            prompt_builder.with_context(s.source2reason[parent_id])
        prompt = prompt_builder.get()
        return prompt

    @staticmethod
    def complete_ranking_prompts(s: RankingStore) -> None:
        """
        Completes the ranking prompts.
        :param s: The ranking store.
        :return: None
        """
        batch_response = complete_prompts(s.ranking_prompts, max_tokens=2000)
        s.ranking_responses = batch_response

    @staticmethod
    def process_ranking_prompts(s: RankingStore) -> None:
        """
        Sets processed prompts in store.
        :param s: The ranking store.
        :return: None
        """
        s.processed_ranking_response: List[List[str]] = ArtifactRankingStep.process_ranked_artifacts(s)

    @staticmethod
    def process_ranked_artifacts(s: RankingStore, add_missing=False) -> List[List[str]]:
        """
        Reads the ranking responses and performs post-processing.
        :param s: The ranking store.
        :param add_missing: Whether to add missing artifact ids.
        :return: Ranked children for each source.
        """
        batch_response = s.ranking_responses

        ranked_target_links = [[] for _ in range(len(s.parent_ids))]
        for source_name, prompt_response in zip(s.parent_ids, batch_response.batch_responses):
            source_index = s.parent_ids.index(source_name)
            related_targets = s.parent2children[source_name]

            response_list = ArtifactRankingStep.convert_response_to_list(prompt_response)  # string response into list
            artifact_indices = ArtifactRankingStep.parse_artifact_indices(response_list)  # processes each artifact id
            artifact_ids = ArtifactRankingStep.translate_indices_to_ids(artifact_indices, related_targets)
            artifact_ids = ArtifactRankingStep.remove_duplicate_ids(artifact_ids)
            ranked_target_links[source_index].extend(artifact_ids)

        if add_missing:
            target_ids = s.all_target_ids
            for r_list in ranked_target_links:
                missing_ids = [t_id for t_id in target_ids if t_id not in r_list]
                random.shuffle(missing_ids)
                r_list.extend(missing_ids)
        return ranked_target_links

    @staticmethod
    def translate_indices_to_ids(artifact_indices: List[str], related_targets: List[str]):
        """
        Translates artifact indices to ids.
        :param artifact_indices: The indices of the artifacts to translate.
        :param related_targets: The target corresponding to indices.
        :return: The translated artifact ids.
        """
        artifact_indices = list(filter(lambda i: len(i) > 0, artifact_indices))
        artifact_indices = list(map(lambda i: int(i), artifact_indices))
        artifact_indices = list(filter(lambda i: i < len(related_targets), artifact_indices))
        artifact_indices = list(map(lambda i: related_targets[i], artifact_indices))
        return artifact_indices

    @staticmethod
    def parse_artifact_indices(raw_artifact_ids: List[str]):
        """
        Performs post-processing on artifact indices.
        :param raw_artifact_ids: The raw ranking responses.
        :return: Processed ids.
        """
        response = []
        for raw_artifact_id in raw_artifact_ids:
            processed = raw_artifact_id
            for s in ID_PROCESSING_STEPS:
                processed = s(processed)
            response.append(processed)
        return response

    @staticmethod
    def convert_response_to_list(r: str):
        """
        Converts string of indices into list of indices.
        :param r: The response string.
        :return: List of ids.
        """
        processed = r
        for s in RESPONSE_PROCESSING_STEPS:
            processed = s(processed)
        return processed

    @staticmethod
    def remove_duplicate_ids(artifact_ids: List[str]):
        """
        Removes duplicate entries.
        :param artifact_ids: The ids to check for duplicates.
        :return: List of artifact ids without duplicates, where first instance is kept.
        """
        new_list = []
        seen = set()
        for artifact_id in artifact_ids:
            if artifact_id not in seen:
                new_list.append(artifact_id)
                seen.add(artifact_id)
        return new_list

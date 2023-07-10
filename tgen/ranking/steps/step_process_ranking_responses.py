import random
from typing import List

from tgen.state.pipeline.abstract_pipeline import AbstractPipelineStep, ArgType
from tgen.state.state import State
from tgen.ranking.ranking_args import RankingArgs
from tgen.ranking.ranking_state import RankingState
from tgen.util.llm_response_util import LLMResponseUtil

ID_PROCESSING_STEPS = [lambda f: f.replace("ID:", ""), lambda f: f.strip()]

RESPONSE_PROCESSING_STEPS = [
    lambda r: LLMResponseUtil.parse(r, "links")[0],
    lambda s: s.replace("ID:", ""),
    lambda s: s.split(",")
]


class ProcessRankingResponses(AbstractPipelineStep[RankingArgs, RankingState]):
    def run(self, args: ArgType, state: State) -> None:
        self.process_ranking_prompts(args, state)

    @staticmethod
    def process_ranking_prompts(args: RankingArgs, state: RankingState) -> None:
        """
        Sets processed prompts in store.
        :param state: The ranking store.
        :return: None
        """
        state.processed_ranking_response: List[List[str]] = ProcessRankingResponses.process_ranked_artifacts(args, state)

    @staticmethod
    def process_ranked_artifacts(args: RankingArgs, state: RankingState, add_missing=False) -> List[List[str]]:
        """
        Reads the ranking responses and performs post-processing.
        :param args: The ranking pipeline configuration.
        :param state: The ranking pipeline state.
        :param add_missing: Whether to add missing artifact ids.
        :return: Ranked children for each source.
        """
        batch_response = state.ranking_responses

        ranked_target_links = [[] for _ in range(len(args.parent_ids))]
        for source_name, prompt_response in zip(args.parent_ids, batch_response.batch_responses):
            source_index = args.parent_ids.index(source_name)
            related_targets = args.parent2children[source_name]

            response_list = ProcessRankingResponses.convert_response_to_list(prompt_response)  # string response into list
            artifact_indices = ProcessRankingResponses.parse_artifact_indices(response_list)  # processes each artifact id
            artifact_ids = ProcessRankingResponses.translate_indices_to_ids(artifact_indices, related_targets)
            artifact_ids = ProcessRankingResponses.remove_duplicate_ids(artifact_ids)
            ranked_target_links[source_index].extend(artifact_ids)

        if add_missing:
            target_ids = state.all_target_ids
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

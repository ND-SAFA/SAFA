from typing import Dict, List

from tgen.common.util.llm_response_util import LLMResponseUtil
from tgen.constants.deliminator_constants import DASH, NEW_LINE
from tgen.ranking.ranking_args import RankingArgs
from tgen.ranking.ranking_state import RankingState
from tgen.state.pipeline.abstract_pipeline import AbstractPipelineStep, ArgType
from tgen.state.state import State

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
        ranked_children, children_explanations = ProcessRankingResponses.process_ranked_artifacts(args, state)
        state.ranked_children = ranked_children
        state.ranked_children_explanations = children_explanations

    @staticmethod
    def process_ranked_artifacts(args: RankingArgs, state: RankingState) -> List[List[str]]:
        """
        Reads the ranking responses and performs post-processing.
        :param args: The ranking pipeline configuration.
        :param state: The ranking pipeline state.
        :param add_missing: Whether to add missing artifact ids.
        :return: Ranked children for each source.
        """
        batch_response = state.ranking_responses

        ranked_children_list = [[] for _ in range(len(args.parent_ids))]
        ranked_children_explanations = [None] * len(args.parent_ids)
        for parent_name, prompt_response in zip(args.parent_ids, batch_response.batch_responses):
            parent_index = args.parent_ids.index(parent_name)
            related_children = state.sorted_parent2children[parent_name]

            # content = LLMResponseUtil.parse(prompt_response, "context")
            related = LLMResponseUtil.parse(prompt_response, "related")[0]
            explanations = ProcessRankingResponses.read_explanations(related, related_children)

            response_list = ProcessRankingResponses.convert_response_to_list(prompt_response)  # string response into list
            artifact_indices = ProcessRankingResponses.parse_artifact_indices(response_list)  # processes each artifact id
            prompt_ranked_children = ProcessRankingResponses.translate_indices_to_ids(artifact_indices, related_children)
            prompt_ranked_children = ProcessRankingResponses.remove_duplicate_ids(prompt_ranked_children)

            prompt_ranked_children_explanations = [explanations[c] if c in explanations else None for c in prompt_ranked_children]

            ranked_children_list[parent_index].extend(prompt_ranked_children)
            ranked_children_explanations[parent_index] = prompt_ranked_children_explanations

        return ranked_children_list, ranked_children_explanations

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

    @staticmethod
    def read_explanations(explanations: str, index_translations: List[str]) -> Dict[str, str]:
        """
        Reads trace link explanations.
        :param explanations: Reads the trace links explanations.
        :param index_translations: The names to use instead of indices.
        :return: Dictionary mapping artifact index to explanation
        """
        elements = explanations.split(NEW_LINE)
        elements = [e.strip() for e in elements]
        elements = [e for e in elements if len(e) > 0]
        elements = [e.split(DASH) for e in elements]
        elements = {e[0].strip(): e[1].strip() for e in elements}
        elements = {int(a_id): e for a_id, e in elements.items()}
        elements = {index_translations[a_id]: e for a_id, e in elements.items()}
        return elements

from typing import Dict, List

from tgen.common.util.llm_response_util import LLMResponseUtil
from tgen.common.util.logging.logger_manager import logger
from tgen.constants.deliminator_constants import DASH, NEW_LINE
from tgen.ranking.ranking_args import RankingArgs
from tgen.ranking.ranking_state import RankingState
from tgen.state.pipeline.abstract_pipeline import AbstractPipelineStep, ArgType
from tgen.state.state import State

ID_PROCESSING_STEPS = [lambda f: f.replace("ID:", ""), lambda f: f.strip()]

RESPONSE_PROCESSING_STEPS = [
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
        :param args: The arguments of the ranking pipeline.
        :param state: The state of the ranking pipeline.
        :return: None
        """
        ranked_children, children_explanations = ProcessRankingResponses.process_ranked_artifacts(args.parent_ids,
                                                                                                  state.ranking_responses.batch_responses,
                                                                                                  state.sorted_parent2children)
        state.ranked_children = ranked_children
        state.ranked_children_explanations = children_explanations

    @staticmethod
    def process_ranked_artifacts(parent_ids: List[str], batch_responses: List[str], sorted_parent2children: Dict[str, List[str]]) -> \
            List[List[str]]:
        """
        Reads the ranking responses and performs post-processing.
        :param parent_ids: The artifact IDs of the parents.
        :param state: The ranking pipeline state.
        :param add_missing: Whether to add missing artifact ids.
        :return: Ranked children for each source.
        """
        ranked_children_list = [[] for _ in range(len(parent_ids))]
        ranked_children_explanations = [None] * len(parent_ids)
        parent2index: Dict[str, int] = {p: i for i, p in enumerate(parent_ids)}
        for parent_name, prompt_response in zip(parent_ids, batch_responses):
            parent_index = parent2index[parent_name]
            related_children = sorted_parent2children[parent_name]

            # Step - Parse and clean
            ID_INDEX = 0
            SUMMARY_INDEX = 1
            EXPLANATION_INDEX = 2
            SCORE_INDEX = 3

            explanation = LLMResponseUtil.parse(prompt_response, "explanation")[0]
            entries = explanation.split("\n")
            entries = [e for e in entries if len(e) > 0]
            entry_pieces = [e.split("|") for e in entries]
            entry_pieces = [[e.strip() for e in entry] for entry in entry_pieces]
            parsed_entries = []
            for e in entry_pieces:
                try:
                    artifact_index = int(e[ID_INDEX])
                    artifact_summary = e[SUMMARY_INDEX]
                    artifact_explanation = e[EXPLANATION_INDEX]
                    artifact_score = float(e[SCORE_INDEX])
                    parsed_entries.append((artifact_index, artifact_summary, artifact_explanation, artifact_score))
                except Exception as e:
                    logger.exception(e)
                    logger.info(f"Unable to parse: {e}")

            # Step - Translate
            entry_pieces = sorted(parsed_entries, key=lambda e: (e[SCORE_INDEX], -e[ID_INDEX]), reverse=True)
            artifact_ids = [related_children[e[ID_INDEX]] for e in entry_pieces]
            artifact_explanations = [e[EXPLANATION_INDEX] for e in entry_pieces]

            # Step - Store results
            ranked_children_list[parent_index].extend(artifact_ids)
            ranked_children_explanations[parent_index] = artifact_explanations

        return ranked_children_list, ranked_children_explanations

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

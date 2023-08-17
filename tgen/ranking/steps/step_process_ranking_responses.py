from typing import Dict, List

from tgen.common.util.json_util import JsonUtil
from tgen.common.util.llm_response_util import LLMResponseUtil
from tgen.constants.deliminator_constants import DASH, NEW_LINE
from tgen.core.trace_output.trace_prediction_output import TracePredictionEntry
from tgen.ranking.ranking_args import RankingArgs
from tgen.ranking.ranking_state import RankingState
from tgen.state.pipeline.abstract_pipeline import AbstractPipelineStep, ArgType
from tgen.state.state import State

ID_PROCESSING_STEPS = [lambda f: f.replace("ID:", ""), lambda f: f.strip()]

RESPONSE_PROCESSING_STEPS = [
    lambda s: s.replace("ID:", ""),
    lambda s: s.split(",")
]
MAX_SCORE = 10


class ArtifactReasoning:

    def __init__(self, artifact_dict: Dict):
        JsonUtil.require_properties(artifact_dict, ["id", "explanation", "score"])
        self.index = int(artifact_dict["id"][0].strip())
        self.explanation = artifact_dict["explanation"][0].strip()
        self.score = float(artifact_dict["score"][0].strip()) / MAX_SCORE
        self.artifact_id = None


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
        children_entries = ProcessRankingResponses.process_ranked_artifacts(args.parent_ids,
                                                                            state.ranking_responses.batch_responses,
                                                                            state.sorted_parent2children)
        state.children_entries = children_entries

    @staticmethod
    def process_ranked_artifacts(parent_ids: List[str], batch_responses: List[str], sorted_parent2children: Dict[str, List[str]]) -> \
            List[TracePredictionEntry]:
        """
        Reads the ranking responses and performs post-processing.
        :param parent_ids: The artifact IDs of the parents.
        :param state: The ranking pipeline state.
        :param add_missing: Whether to add missing artifact ids.
        :return: Ranked children for each source.
        """
        parent2index: Dict[str, int] = {p: i for i, p in enumerate(parent_ids)}
        child_entries = []
        for parent_name, prompt_response in zip(parent_ids, batch_responses):
            related_children = sorted_parent2children[parent_name]

            artifact_dicts = LLMResponseUtil.parse(prompt_response, "artifact", is_nested=True)
            parsed_entries = []
            for a_parsed_dict in artifact_dicts:
                a_reasoning = ArtifactReasoning(a_parsed_dict)
                a_reasoning.artifact_id = related_children[a_reasoning.index]
                parsed_entries.append(a_reasoning)

            parsed_entries: List[ArtifactReasoning] = sorted(parsed_entries, key=lambda a: (a.score, -a.index), reverse=True)

            # Step - Store results
            for e in parsed_entries:
                child_entry = TracePredictionEntry(
                    source=e.artifact_id,
                    target=parent_name,
                    score=e.score,
                    explanation=e.explanation
                )
                child_entries.append(child_entry)

        return child_entries

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

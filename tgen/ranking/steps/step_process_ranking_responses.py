from typing import Dict, List

from tgen.common.util.json_util import JsonUtil
from tgen.constants.ranking_constants import RANKING_ARTIFACT_TAG, RANKING_EXPLANATION_TAG, RANKING_ID_TAG, \
    RANKING_MAX_SCORE, RANKING_SCORE_TAG
from tgen.core.trace_output.trace_prediction_output import TracePredictionEntry
from tgen.data.dataframes.artifact_dataframe import ArtifactKeys
from tgen.ranking.ranking_args import RankingArgs
from tgen.ranking.ranking_state import RankingState
from tgen.state.pipeline.abstract_pipeline import AbstractPipelineStep, ArgType
from tgen.state.state import State

ID_PROCESSING_STEPS = [lambda f: f.replace("ID:", ""), lambda f: f.strip()]


class ArtifactReasoning:

    def __init__(self, artifact_dict: Dict):
        JsonUtil.require_properties(artifact_dict, [ArtifactKeys.ID.value, RANKING_EXPLANATION_TAG, RANKING_SCORE_TAG])
        self.index = artifact_dict[RANKING_ID_TAG][0]
        self.explanation = artifact_dict[RANKING_EXPLANATION_TAG][0].strip()
        self.score = artifact_dict[RANKING_SCORE_TAG][0] / RANKING_MAX_SCORE
        self.artifact_id = None


class ProcessRankingResponses(AbstractPipelineStep[RankingArgs, RankingState]):
    def run(self, args: ArgType, state: State) -> None:
        self.process_ranking_prompts(args, state)

    def process_ranking_prompts(self, args: RankingArgs, state: RankingState) -> List[TracePredictionEntry]:
        """
        Reads the ranking responses and performs post-processing.
        :param args: The ranking pipeline arguments.
        :param state: The ranking pipeline state.
        :return: Ranked children for each source.
        """
        parent_ids = args.parent_ids
        batch_responses = state.ranking_responses.batch_responses
        sorted_parent2children = state.sorted_parent2children
        parent2index: Dict[str, int] = {p: i for i, p in enumerate(parent_ids)}
        child_entries = []
        for parent_name, prompt_response in zip(parent_ids, batch_responses):
            related_children = sorted_parent2children[parent_name]
            parent_index = parent2index[parent_name]
            r = state.prompt_builders[parent_index].parse_responses(prompt_response)
            prompt_id = state.prompt_builders[parent_index].get_all_prompts()[-1].id
            parsed_tags = r[prompt_id]
            artifact_dicts = parsed_tags[RANKING_ARTIFACT_TAG]
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
        state.children_entries = child_entries
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

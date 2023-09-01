from typing import Any, Callable, Dict, List, Optional

from tgen.common.constants.tracing.ranking_constants import RANKING_ARTIFACT_TAG, RANKING_EXPLANATION_TAG, RANKING_ID_TAG, \
    RANKING_MAX_SCORE, RANKING_SCORE_TAG
from tgen.common.util.json_util import JsonUtil
from tgen.common.util.logging.logger_manager import logger
from tgen.core.trace_output.trace_prediction_output import TracePredictionEntry
from tgen.data.dataframes.artifact_dataframe import ArtifactKeys
from tgen.data.dataframes.trace_dataframe import TraceDataFrame
from tgen.state.pipeline.abstract_pipeline import AbstractPipelineStep, ArgType
from tgen.state.state import State
from tgen.tracing.ranking.ranking_args import RankingArgs
from tgen.tracing.ranking.ranking_state import RankingState

ID_PROCESSING_STEPS = [lambda f: f.replace("ID:", ""), lambda f: f.strip()]


class ArtifactReasoning:

    def __init__(self, artifact_dict: Dict):
        """
        Stores the reasoning of the LLM for each artifact
        :param artifact_dict: Contains the reasoning of the LLM for each artifact
        """
        JsonUtil.require_properties(artifact_dict, [ArtifactKeys.ID.value])
        self.index = self.get_optional(artifact_dict, RANKING_ID_TAG)
        self.explanation = self.get_optional(artifact_dict, RANKING_EXPLANATION_TAG, lambda s: s.strip())
        self.score = self.get_optional(artifact_dict, RANKING_SCORE_TAG, lambda s: s / RANKING_MAX_SCORE, default_value=0)
        self.artifact_id = None

    @staticmethod
    def get_optional(a_dict: Dict, key_name: str, post_process: Callable = None, default_value=None) -> Optional[Any]:
        """
        Returns optional value from dictionary.
        :param a_dict: The dictionary to retrieve the value from.
        :param key_name: The name of the optional key.
        :param post_process: Any operation to perform after value is retrieved, if it exists.
        :param default_value: The value to use if none exists.
        :return: The optional value.
        """
        if post_process is None:
            post_process = lambda p: p
        optional_value = a_dict.get(key_name, [])
        if len(optional_value) == 0:
            optional_value = [default_value]
        if optional_value:
            value = optional_value[0]
            value = post_process(value)
            return value
        return None


class ProcessRankingResponses(AbstractPipelineStep[RankingArgs, RankingState]):
    def _run(self, args: ArgType, state: State) -> None:
        self.process_ranking_prompts(args, state)

    @staticmethod
    def process_ranking_prompts(args: RankingArgs, state: RankingState) -> List[TracePredictionEntry]:
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
        child_entries_set = set()
        for parent_name, prompt_response in zip(parent_ids, batch_responses):
            related_children = sorted_parent2children[parent_name]
            parent_index = parent2index[parent_name]
            r = state.prompt_builders[parent_index].parse_responses(prompt_response)
            prompt_id = state.prompt_builders[parent_index].get_all_prompts()[-1].id
            parsed_tags = r[prompt_id]
            artifact_dicts = parsed_tags[RANKING_ARTIFACT_TAG]
            parsed_entries = []
            for a_parsed_dict in artifact_dicts:
                try:
                    a_reasoning = ArtifactReasoning(a_parsed_dict)
                    a_reasoning.artifact_id = related_children[a_reasoning.index]
                    parsed_entries.append(a_reasoning)
                except Exception as e:
                    logger.exception(e)
                    logger.info(f"Unable to parse: {a_parsed_dict}")

            parsed_entries: List[ArtifactReasoning] = sorted(parsed_entries, key=lambda a: (a.score, -a.index), reverse=True)

            # Step - Store results
            for e in parsed_entries:
                child_name = e.artifact_id
                trace_id = TraceDataFrame.generate_link_id(source_id=child_name, target_id=parent_name)
                if trace_id in child_entries_set:
                    continue
                child_entry = TracePredictionEntry(
                    source=child_name,
                    target=parent_name,
                    score=e.score,
                    explanation=e.explanation
                )
                child_entries.append(child_entry)
                child_entries_set.add(trace_id)
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

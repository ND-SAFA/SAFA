from typing import Dict, List, Set, Any

from tgen.common.constants.deliminator_constants import NEW_LINE
from tgen.common.constants.tracing.ranking_constants import RANKING_ID_TAG, \
    RANKING_MAX_SCORE, RANKING_SCORE_TAG
from tgen.common.util.json_util import JsonUtil
from tgen.common.util.logging.logger_manager import logger
from tgen.core.trace_output.trace_prediction_output import TracePredictionEntry
from tgen.data.dataframes.artifact_dataframe import ArtifactKeys
from tgen.data.dataframes.trace_dataframe import TraceDataFrame, TraceKeys
from tgen.state.pipeline.abstract_pipeline import AbstractPipelineStep, ArgType
from tgen.state.state import State
from tgen.tracing.ranking.common.ranking_args import RankingArgs
from tgen.tracing.ranking.common.ranking_state import RankingState

ID_PROCESSING_STEPS = [lambda f: f.replace("ID:", ""), lambda f: f.strip()]


class ArtifactReasoning:

    def __init__(self, artifact_dict: Dict):
        """
        Stores the reasoning of the LLM for each artifact
        :param artifact_dict: Contains the reasoning of the LLM for each artifact
        """
        JsonUtil.require_properties(artifact_dict, [ArtifactKeys.ID.value])
        self.index = self.get_attr(RANKING_ID_TAG, artifact_dict, pop=True)
        self.score = self.get_attr(RANKING_SCORE_TAG, artifact_dict, 0.0, pop=True) / RANKING_MAX_SCORE
        self.explanation = self.construct_explanation(artifact_dict)
        self.artifact_id = None

    @staticmethod
    def construct_explanation(explanation_parts: Dict) -> str:
        """
        Constructs the explanation from its parts
        :param explanation_parts: Dictionary mapping explanation part name and content
        :return: The explanation as a str
        """
        explanation_values = [ArtifactReasoning.get_attr(name, explanation_parts) for name in explanation_parts.keys()]
        return NEW_LINE.join([v for v in explanation_values if v])

    @staticmethod
    def get_attr(attr_name: str, artifact_dict: Dict, default: Any = None, expected_list: bool = False, pop: bool = False) -> Any:
        """
        Gets an attributes from the artifact dict
        :param attr_name: The key to retrieve
        :param artifact_dict: The artifact dict to retrieve it from
        :param default: Default value if it doesnt exist
        :param expected_list: If True, the value of the attr is expected to be a list
        :param pop: If True, pops the value during retrieval
        :return: The value of the attr
        """
        if pop:
            val = artifact_dict.pop(attr_name) if attr_name in attr_name else default
        else:
            val = artifact_dict.get(attr_name, default)
        if isinstance(val, list) and not expected_list:
            val = val[0] if val else default
        return val


class ProcessRankingResponsesStep(AbstractPipelineStep[RankingArgs, RankingState]):

    def _run(self, args: ArgType, state: State) -> None:
        """
        Process the responses from the model in the previous step
        :param args: The args for ranking
        :param state: The current state of the ranking
        :return: None
        """
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
        ranking_responses = state.ranking_responses
        sorted_parent2children = state.sorted_parent2children
        all_entries = []
        for parent_name, prompt_response in zip(parent_ids, ranking_responses):
            related_children = [entry[TraceKeys.SOURCE] for entry in sorted_parent2children[parent_name]]
            parsed_entries, unidentified_entries, parsed_artifact_ids = [], [], set()
            for i, artifact_res in enumerate(prompt_response):
                try:
                    a_reasoning = ArtifactReasoning(artifact_res)
                    if a_reasoning.index is None:
                        a_reasoning.index = i
                        a_reasoning.artifact_id = related_children[a_reasoning.index]
                        unidentified_entries.append(a_reasoning)
                    elif a_reasoning.index not in parsed_artifact_ids:
                        a_reasoning.artifact_id = related_children[a_reasoning.index]
                        parsed_entries.append(a_reasoning)
                        parsed_artifact_ids.add(a_reasoning.artifact_id)
                except Exception as e:
                    logger.exception(e)
                    logger.info(f"Unable to parse: {artifact_res}")
            n_unidentified = ProcessRankingResponsesStep._identify_unknown_a_reasoning(unidentified_entries, parsed_entries,
                                                                                       parsed_artifact_ids)
            ProcessRankingResponsesStep._log_processing_warning(n_unidentified, parent_name, "unidentified")
            n_missing = len(related_children) - len(parsed_artifact_ids)
            ProcessRankingResponsesStep._log_processing_warning(n_missing, parent_name, "missing")
            parsed_entries: List[ArtifactReasoning] = sorted(parsed_entries, key=lambda a: (a.score, -a.index), reverse=True)

            # Step - Store results
            child_entries = ProcessRankingResponsesStep._create_trace_prediction_entries(parsed_entries, parent_name)
            all_entries.extend(child_entries)
        state.children_entries = all_entries
        return all_entries

    @staticmethod
    def _identify_unknown_a_reasoning(unidentified_entries: List[ArtifactReasoning], parsed_entries: List[ArtifactReasoning],
                                      parsed_artifact_ids: Set) -> int:
        """
        Tries to add any unidentified artifact reasoning to the parsed entries
        :param unidentified_entries: The list of unidentified entries
        :param parsed_entries: The list of already identified entries
        :param parsed_artifact_ids: The list of artifact ids that were identified
        :return: The number of remaining unidentified artifact reasoning
        """
        n_unidentified = 0
        for a_reasoning in unidentified_entries:
            if a_reasoning.artifact_id not in parsed_artifact_ids:
                parsed_entries.append(a_reasoning)
                parsed_artifact_ids.add(a_reasoning.artifact_id)
            else:
                n_unidentified += 1
        return n_unidentified

    @staticmethod
    def _create_trace_prediction_entries(parsed_entries: List[ArtifactReasoning], parent_name: str) -> List[TracePredictionEntry]:
        """
        Creates the trace prediction entries from the artifact reasoning (parsed from response)
        :param parsed_entries: The artifact reasoning parsed from the LLM response
        :param parent_name: The name of the parent artifact
        :return: The artifact reasoning objects converted to trace prediction entires
        """
        child_entries = []
        for e in parsed_entries:
            child_name = e.artifact_id
            trace_id = TraceDataFrame.generate_link_id(source_id=child_name, target_id=parent_name)
            child_entry = TracePredictionEntry(
                id=trace_id,
                source=child_name,
                target=parent_name,
                score=e.score,
                explanation=e.explanation
            )
            child_entries.append(child_entry)
        return child_entries

    @staticmethod
    def _log_processing_warning(n_affected_artifacts: int, parent_name: str, problem: str = "missing") -> None:
        """
        Logs any problematic artifacts (e.g. missing or unidentified) for a given parent
        :param n_affected_artifacts: The total number of affected artifacts
        :param parent_name: The name of the parent
        :param problem: The problem with the artifacts (e.g. missing or unidentified)
        :return: None
        """
        if n_affected_artifacts > 0:
            logger.warning(f"Found {n_affected_artifacts} {problem} artifacts after parsing children of {parent_name}")

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

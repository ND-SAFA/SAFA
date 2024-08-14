from typing import List, Dict

from tgen.common.constants.ranking_constants import DEFAULT_SCORE
from common_resources.tools.t_logging.logger_manager import logger
from tgen.common.objects.trace import Trace
from common_resources.tools.util.enum_util import EnumDict
from common_resources.tools.util.math_util import MathUtil
from common_resources.data.dataframes.trace_dataframe import TraceDataFrame
from common_resources.data.keys.structure_keys import TraceKeys
from tgen.pipeline.abstract_pipeline_step import AbstractPipelineStep
from tgen.tracing.ranking.common.artifact_reasoning import ArtifactReasoning
from tgen.tracing.ranking.common.ranking_args import RankingArgs
from tgen.tracing.ranking.common.ranking_state import RankingState

ID_PROCESSING_STEPS = [lambda f: f.replace("ID:", ""), lambda f: f.strip()]


class ProcessRankingResponsesStep(AbstractPipelineStep[RankingArgs, RankingState]):

    def _run(self, args: RankingArgs, state: RankingState) -> None:
        """
        Process the responses from the model in the previous step
        :param args: The args for ranking
        :param state: The current state of the ranking
        :return: None
        """
        self.process_ranking_prompts(args, state)

    @staticmethod
    def process_ranking_prompts(args: RankingArgs, state: RankingState) -> List[Trace]:
        """
        Reads the ranking responses and performs post-processing.
        :param args: The ranking pipeline arguments.
        :param state: The ranking pipeline state.
        :return: Ranked children for each source.
        """
        parent_ids = args.parent_ids
        ranking_responses = state.ranking_responses
        sorted_parent2children = state.get_current_parent2children()
        all_entries = []
        for parent_name, prompt_response in zip(parent_ids, ranking_responses):
            related_children = [entry[TraceKeys.child_label()] for entry in sorted_parent2children[parent_name]]
            parsed_id_to_reasoning = ProcessRankingResponsesStep._create_artifact_reasonings(prompt_response,
                                                                                             parent_name,
                                                                                             related_children)
            ProcessRankingResponsesStep._add_missing_artifact_reasonings(parsed_id_to_reasoning, sorted_parent2children[parent_name],
                                                                         args.weight_of_embedding_scores)
            child_entries = ProcessRankingResponsesStep._create_trace_prediction_entries(list(parsed_id_to_reasoning.values()),
                                                                                         parent_name)
            all_entries.extend(child_entries)
        state.candidate_entries = all_entries
        return all_entries

    @staticmethod
    def _create_artifact_reasonings(prompt_response: List[Dict],
                                    parent_name: str,
                                    related_children: List) -> Dict[str, ArtifactReasoning]:
        """
        Creates artifact reasoning objects from the prompt response
        :param prompt_response: The response from the model
        :param parent_name: The name of the parent artifact
        :param related_children: A list of related children ids
        :return: A list of parsed artifact reasoning and unidentified artifact reasoning, and the set of successful parsed artifact ids
        """
        parsed_id_to_reasoning, unidentified_reasonings = {}, []
        for i, artifact_res in enumerate(prompt_response):
            try:
                artifact_reasoning = ArtifactReasoning(artifact_res)
                if artifact_reasoning.index is None:
                    artifact_reasoning.index = i
                    artifact_reasoning.artifact_id = related_children[artifact_reasoning.index]
                    unidentified_reasonings.append(artifact_reasoning)
                elif artifact_reasoning.index not in parsed_id_to_reasoning:
                    artifact_reasoning.artifact_id = related_children[artifact_reasoning.index]
                    parsed_id_to_reasoning[artifact_reasoning.artifact_id] = artifact_reasoning
            except Exception as e:
                logger.exception(e)
                logger.info(f"Unable to parse: {artifact_res}")

        n_unidentified = ProcessRankingResponsesStep._identify_unknown_artifact_reasoning(unidentified_reasonings,
                                                                                          parsed_id_to_reasoning)
        ProcessRankingResponsesStep._log_processing_warning(n_unidentified, parent_name, "unidentified")
        n_missing = len(related_children) - len(parsed_id_to_reasoning)
        ProcessRankingResponsesStep._log_processing_warning(n_missing, parent_name, "missing")
        return parsed_id_to_reasoning

    @staticmethod
    def _identify_unknown_artifact_reasoning(unidentified_reasonings: List[ArtifactReasoning],
                                             parsed_id_to_reasoning: Dict[str, ArtifactReasoning]) -> int:
        """
        Tries to add any unidentified artifact reasoning to the parsed artifact reasoning
        :param unidentified_reasonings: The list of unidentified artifact reasoning
        :param parsed_id_to_reasoning: Dictionary mapping identified artifact id to its artifact reasoning
        :return: The number of remaining unidentified artifact reasoning
        """
        n_unidentified = 0
        for artifact_reasoning in unidentified_reasonings:
            if artifact_reasoning.artifact_id not in parsed_id_to_reasoning:
                parsed_id_to_reasoning[artifact_reasoning.artifact_id] = artifact_reasoning
            else:
                n_unidentified += 1
        return n_unidentified

    @staticmethod
    def _add_missing_artifact_reasonings(parsed_id_to_reasoning: Dict[str, ArtifactReasoning],
                                         sorted_children: List[EnumDict],
                                         weight_of_embedding_scores: float) -> None:
        """
        Fills in missing a reasonings using the sorted children
        :param parsed_id_to_reasoning: A dictionary mapping artifact id to its parsed a reasoning
        :param sorted_children: The list of original sorted children (likely by embedding)
        :param weight_of_embedding_scores: The weight of the embeddings score on the overall score
        :return: None
        """
        for entry in sorted_children:
            child_id = entry[TraceKeys.SOURCE]
            if child_id not in parsed_id_to_reasoning:
                parsed_id_to_reasoning[child_id] = ArtifactReasoning(artifact_id=child_id, score=entry[TraceKeys.SCORE])
            artifact_reasoning = parsed_id_to_reasoning[child_id]
            if artifact_reasoning.score is None or artifact_reasoning.score == DEFAULT_SCORE:
                artifact_reasoning.score = entry[TraceKeys.SCORE]
            else:
                artifact_reasoning.score = MathUtil.calculate_weighted_score(scoreA=entry[TraceKeys.SCORE],
                                                                             scoreB=artifact_reasoning.score,
                                                                             weight_of_scoreA=weight_of_embedding_scores)

    @staticmethod
    def _create_trace_prediction_entries(parsed_entries: List[ArtifactReasoning], parent_name: str) -> List[Trace]:
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
            child_entry = EnumDict(Trace(
                id=trace_id,
                source=child_name,
                target=parent_name,
                score=e.score,
                explanation=e.explanation
            ))
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

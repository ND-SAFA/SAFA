from typing import List

from gen_common.graph.graph_runner import GraphRunner
from gen_common.graph.io.graph_args import GraphArgs

from gen.health.contradiction.contradiction_args import ContradictionsArgs
from gen.health.contradiction.contradiction_graph import ContradictionsGraph
from gen.health.contradiction.contradiction_prompts import CONTRADICTIONS_QUESTION
from gen.health.contradiction.contradiction_result import ContradictionResult


class ContradictionsDetector:

    def __init__(self, args: ContradictionsArgs):
        """
        Handles detecting contradictions in artifacts.
        :param args: Arguments to the detector
        """
        self.args = args

    def detect(self, query_ids: List[str]) -> List[ContradictionResult]:
        """
        Determines whether a given artifact has any contradictions
        :param query_ids: The id of the artifact to detect contradictions for.
        :return A list of ids that conflict with the artifact (empty list if none conflict) and the explanation for why.
        """
        assert all([q_id in self.args.dataset.artifact_df for q_id in query_ids]), f"Queries contain unknown ids: {query_ids}"

        runner = GraphRunner(ContradictionsGraph.DEFINITION)
        graph_args = GraphArgs(dataset=self.args.dataset)
        user_questions = [CONTRADICTIONS_QUESTION.format(q_id) for q_id in query_ids]
        results: List[ContradictionResult] = runner.run_multi(args=graph_args, user_question=user_questions,
                                                              artifacts_referenced_in_question=query_ids)
        [result.conflicting_ids.append(q_id) for q_id, result in zip(query_ids, results) if result and result.conflicting_ids]
        return results

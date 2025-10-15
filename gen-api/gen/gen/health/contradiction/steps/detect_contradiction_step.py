from typing import List

from gen_common.graph.graph_runner import GraphRunner
from gen_common.graph.io.graph_args import GraphArgs
from gen_common.pipeline.abstract_pipeline_step import AbstractPipelineStep

from gen.health.contradiction.contradiction_graph import ContradictionsGraph
from gen.health.contradiction.contradiction_prompts import CONTRADICTIONS_QUESTION
from gen.health.contradiction.contradiction_result import ContradictionResult
from gen.health.contradiction.contradiction_state import ContradictionState
from gen.health.health_args import HealthArgs
from gen.health.health_state import HealthState


class DetectContradictionStep(AbstractPipelineStep[HealthArgs, HealthState]):

    def _run(self, args: HealthArgs, state: ContradictionState) -> None:
        """
        Detects contradictions in query artifacts.
        :param args: Health args containing artifacts.
        :param state: State to store contradiction in.
        :return: None
        """
        query_ids = args.query_ids
        assert all([q_id in args.dataset.artifact_df for q_id in query_ids]), f"Queries contain unknown ids: {query_ids}"

        runner = GraphRunner(ContradictionsGraph.DEFINITION)
        graph_args = GraphArgs(dataset=args.dataset)
        user_questions = [CONTRADICTIONS_QUESTION.format(q_id) for q_id in query_ids]
        results: List[ContradictionResult] = runner.run_multi(args=graph_args, user_question=user_questions,
                                                              artifacts_referenced_in_question=query_ids)
        [result.conflicting_ids.append(q_id)
         for q_id, result in zip(query_ids, results)
         if result and len(result.conflicting_ids) > 0]

        state.contradictions = results

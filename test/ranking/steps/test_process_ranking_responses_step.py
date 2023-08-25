from unittest import TestCase

from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame
from tgen.data.dataframes.trace_dataframe import TraceKeys
from tgen.models.llm.llm_responses import GenerationResponse
from tgen.tracing.ranking.ranking_args import RankingArgs
from tgen.tracing.ranking.ranking_state import RankingState
from tgen.tracing.ranking.steps.step_create_ranking_prompts import CreateRankingPrompts
from tgen.tracing.ranking.steps.step_process_ranking_responses import ProcessRankingResponses


class TestProcessRankingResponsesStep(TestCase):
    RESPONSE = (
        "<explanation>"
        "0 | EXPLANATION_1 | 1\n"
        "1 | EXPLANATION_2 | 2\n"
        "2 | EXPLANATION_3 | 3\n"
        "3 | EXPLANATION_4 | 4\n"
        "</explanation>"
    )

    def test_process_ranked_artifacts(self):
        """
        Tests that each artifact id is processed and missing ids are added back in
        """
        parent_ids = ["parent"]
        children_ids = ["1", "2", "3", "4"]
        args = RankingArgs(parent_ids=parent_ids, children_ids=children_ids, artifact_df=ArtifactDataFrame())
        state = RankingState(sorted_parent2children={"parent": children_ids},
                             ranking_responses=GenerationResponse(batch_responses=[self.RESPONSE]))
        prompt_builder = CreateRankingPrompts.create_ranking_prompt_builder(args, state, parent_body="")
        state.prompt_builders.append(prompt_builder)
        trace_prediction_entries = ProcessRankingResponses.process_ranking_prompts(args, state)

        # Test children ranked correctly
        for i in range(4, 1):
            entry = trace_prediction_entries[i]
            self.assertEqual(f"{i}", entry[TraceKeys.SOURCE.value])
            self.assertEqual(f"EXPLANATION_{i + 1}", entry[TraceKeys.SOURCE.value])

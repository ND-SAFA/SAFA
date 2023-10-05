from unittest import TestCase

from tgen.data.dataframes.artifact_dataframe import ArtifactDataFrame
from tgen.data.dataframes.trace_dataframe import TraceKeys
from tgen.data.tdatasets.prompt_dataset import PromptDataset
from tgen.models.llm.llm_responses import GenerationResponse
from tgen.tracing.ranking.common.ranking_util import RankingUtil
from tgen.tracing.ranking.common.ranking_args import RankingArgs
from tgen.tracing.ranking.common.ranking_state import RankingState
from tgen.tracing.ranking.steps.complete_ranking_prompts_step import CompleteRankingPromptsStep
from tgen.tracing.ranking.steps.process_ranking_responses_step import ProcessRankingResponsesStep


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
        args = RankingArgs(parent_ids=parent_ids, children_ids=children_ids, dataset=PromptDataset(artifact_df=ArtifactDataFrame()))
        state = RankingState(sorted_parent2children={"parent": [RankingUtil.create_entry("parent", c) for c in children_ids]},
                             ranking_responses=GenerationResponse(batch_responses=[self.RESPONSE]))
        state.prompt_builder = CompleteRankingPromptsStep.create_ranking_prompt_builder(state)
        trace_prediction_entries = ProcessRankingResponsesStep.process_ranking_prompts(args, state)

        # Test children ranked correctly
        for i in range(4, 1):
            entry = trace_prediction_entries[i]
            self.assertEqual(f"{i}", entry[TraceKeys.SOURCE.value])
            self.assertEqual(f"EXPLANATION_{i + 1}", entry[TraceKeys.SOURCE.value])


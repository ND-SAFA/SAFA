from tgen.pipeline.abstract_pipeline import AbstractPipelineStep
from typing import List

from tgen.common.objects.trace import Trace
from tgen.common.util.file_util import FileUtil
from tgen.data.keys.structure_keys import TraceKeys
from tgen.hgen.common.hgen_util import HGenUtil
from tgen.hgen.hgen_args import HGenArgs
from tgen.hgen.hgen_state import HGenState
from tgen.tracing.ranking.common.ranking_args import RankingArgs
from tgen.tracing.ranking.common.ranking_state import RankingState
from tgen.tracing.ranking.steps.create_explanations_step import CreateExplanationsStep


class GenerateExplanationsForLinksStep(AbstractPipelineStep[HGenArgs, HGenState]):

    def _run(self, args: HGenArgs, state: HGenState) -> None:
        """
        Generates trace links between the new generated artifacts and the source artifacts
        :param state: The current state of hgen at this point in time
        :param args: The arguments and current state of HGEN.
        :return: None
        """

        if not args.generate_trace_links or not args.generate_explanations:
            return

        export_dir = FileUtil.safely_join_paths(HGenUtil.get_ranking_dir(state.export_dir), "explanations")
        pipeline_args = RankingArgs(run_name="explanations", parent_ids=[], children_ids=[],
                                    weight_of_explanation_scores=0, export_dir=export_dir,
                                    dataset=state.all_artifacts_dataset, selection_method=None,
                                    types_to_trace=(args.source_type, args.target_type), generate_explanations=True)
        pipeline_args.update_llm_managers_with_state(state)

        missing_explanations = [trace for trace in state.selected_predictions if not trace.get(TraceKeys.EXPLANATION)]
        have_explanations = [trace for trace in state.selected_predictions if trace.get(TraceKeys.EXPLANATION)]
        pipeline_state = RankingState(candidate_entries=missing_explanations)
        CreateExplanationsStep().run(pipeline_args, pipeline_state)
        selected_traces = pipeline_state.get_current_entries()
        state.selected_predictions = have_explanations + selected_traces

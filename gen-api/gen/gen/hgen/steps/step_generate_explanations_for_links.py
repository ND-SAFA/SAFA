from typing import List

from gen_common.data.keys.structure_keys import TraceKeys
from gen_common.data.objects.trace import Trace
from gen_common.infra.t_logging.logger_manager import logger
from gen_common.pipeline.abstract_pipeline_step import AbstractPipelineStep
from gen_common.traceability.ranking.common.ranking_args import RankingArgs
from gen_common.traceability.ranking.common.ranking_state import RankingState
from gen_common.traceability.ranking.steps.create_explanations_step import CreateExplanationsStep
from gen_common.util.enum_util import EnumDict
from gen_common.util.file_util import FileUtil

from gen.hgen.common.hgen_util import HGenUtil
from gen.hgen.hgen_args import HGenArgs
from gen.hgen.hgen_state import HGenState


class GenerateExplanationsForLinksStep(AbstractPipelineStep[HGenArgs, HGenState]):

    def _run(self, args: HGenArgs, state: HGenState) -> None:
        """
        Generates trace links between the new generated artifacts and the source artifacts
        :param state: The current state of hgen at this point in time
        :param args: The arguments and current state of HGEN.
        :return: None
        """

        if not args.generate_explanations:
            return

        export_dir = FileUtil.safely_join_paths(HGenUtil.get_ranking_dir(state.export_dir), "explanations")
        pipeline_args = RankingArgs(run_name="explanations", parent_ids=[], children_ids=[],
                                    weight_of_explanation_scores=0, export_dir=export_dir,
                                    dataset=state.selected_artifacts_dataset, selection_method=None,
                                    types_to_trace=(args.source_type, args.target_type), generate_explanations=True)
        pipeline_args.update_llm_managers_with_state(state)

        missing_explanations = self._find_missing_explanations(state.selected_predictions)
        have_explanations = [trace for trace in state.selected_predictions if trace.get(TraceKeys.EXPLANATION)]
        if missing_explanations:
            pipeline_state = RankingState(candidate_entries=missing_explanations)
            CreateExplanationsStep().run(pipeline_args, pipeline_state)
            selected_traces = pipeline_state.get_current_entries()
            selected_predictions = have_explanations + selected_traces
        if not self._find_missing_explanations(selected_predictions):
            state.selected_predictions = selected_predictions
        else:
            logger.error("Traces are still missing explanations. Ensure LLM responses have been deleted.")

    @staticmethod
    def _find_missing_explanations(selected_predictions: List[Trace]) -> List[EnumDict]:
        """
        Finds all traces that are missing explanations
        :param selected_predictions: List of links that have been selected
        :return: A list of all traces that are missing explanations
        """
        return [trace for trace in selected_predictions if not trace.get(TraceKeys.EXPLANATION)]

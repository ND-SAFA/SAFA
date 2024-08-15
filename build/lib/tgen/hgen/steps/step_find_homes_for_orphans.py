from typing import Any, Dict, List, Set

from common_resources.data.objects.trace import Trace
from common_resources.tools.util.enum_util import EnumDict
from common_resources.tools.util.file_util import FileUtil
from common_resources.data.keys.structure_keys import TraceKeys
from tgen.hgen.hgen_args import HGenArgs
from tgen.hgen.hgen_state import HGenState
from tgen.pipeline.abstract_pipeline_step import AbstractPipelineStep
from tgen.tracing.ranking.common.ranking_args import RankingArgs
from tgen.tracing.ranking.common.ranking_util import RankingUtil
from tgen.tracing.ranking.embedding_ranking_pipeline import EmbeddingRankingPipeline


class FindHomesForOrphansStep(AbstractPipelineStep[HGenArgs, HGenState]):

    def _run(self, args: HGenArgs, state: HGenState) -> None:
        """
        Generates trace links for all orphan artifacts
        :param state: The current state of hgen at this point in time
        :param args: The arguments and current state of HGEN.
        :return: None
        """
        if args.min_orphan_score_threshold is not None:
            state.selected_predictions = self.place_orphans_in_homes(args, state, trace_predictions=state.trace_predictions,
                                                                     trace_selections=state.selected_predictions)

    @staticmethod
    def place_orphans_in_homes(args: HGenArgs,
                               state: HGenState,
                               trace_predictions: List[EnumDict],
                               trace_selections: List[EnumDict]) -> List[EnumDict]:
        """
        Links orphan children to their top parent.
        :param args: The arguments of the HGEN pipeline defining the parent and child types.
        :param state: The state of the pipeline containing the contents of the child/parent artifacts.
        :param trace_predictions: All trace link predictions.
        :param trace_selections:  List of selected trace links.
        :return: None. Selections are added to list.
        """
        all_children_ids = list(state.selected_artifacts_dataset.artifact_df.get_artifacts_by_type(args.source_layer_ids).index)
        all_parent_ids = list(state.selected_artifacts_dataset.artifact_df.get_artifacts_by_type(args.target_type).index)

        child2predictions = RankingUtil.group_trace_predictions(trace_predictions, TraceKeys.child_label())
        child2selected = RankingUtil.group_trace_predictions(trace_selections, TraceKeys.child_label())

        orphans = FindHomesForOrphansStep.find_orphan_artifacts(all_children_ids, child2predictions, child2selected, trace_selections)
        if not orphans:
            return trace_selections

        run_name = "Placing Orphans in Homes"
        export_dir = FileUtil.safely_join_paths(args.export_dir, "orphan_ranking")
        pipeline_args = RankingArgs(run_name=run_name,
                                    dataset=state.selected_artifacts_dataset,
                                    parent_ids=all_parent_ids,
                                    children_ids=list(orphans),
                                    export_dir=export_dir,
                                    types_to_trace=(args.source_type, args.target_type),
                                    generate_explanations=False,
                                    selection_method=None,
                                    embeddings_manager=state.embedding_manager)
        pipeline = EmbeddingRankingPipeline(pipeline_args,
                                            skip_summarization=True)
        pipeline.run()

        orphan2predictions = RankingUtil.group_trace_predictions(pipeline.state.selected_entries, TraceKeys.child_label())
        for orphan_id, orphan_preds in orphan2predictions.items():
            top_prediction = sorted(orphan_preds, key=lambda t: t[TraceKeys.SCORE], reverse=True)[0]
            if top_prediction[TraceKeys.SCORE] >= args.min_orphan_score_threshold:
                trace_selections.append(top_prediction)

        return trace_selections

    @staticmethod
    def find_orphan_artifacts(children_ids: List[Any], child2predictions: Dict[Any, List[Trace]],
                              child2selected: Dict[Any, List[Trace]], trace_selections: List[Trace]) -> Set[str]:
        """
        Finds the orphan artifacts using the trace predictions and selections to establish which artifacts have trace links.
        :param children_ids: List of children artifact ids.
        :param child2predictions: Map of child id to its predictions.
        :param child2selected:  Map of child id to its selected traces.
        :param trace_selections: List of selected traces links, used to update selections if link is available.
        :param min_score: The minimum score at which an orphan can be linked
        :return: List of orphan artifact ids.
        """
        orphans = set()
        for child in children_ids:
            predicted_child_links = child2predictions.get(child, [])
            selected_child_links = child2selected.get(child, [])

            if len(selected_child_links) > 0:
                continue
            if len(predicted_child_links) > 0:
                top_prediction = sorted(predicted_child_links, key=lambda t: t[TraceKeys.SCORE], reverse=True)[0]
                trace_selections.append(top_prediction)
                continue
            orphans.add(child)

        return orphans

from trace import Trace
from typing import Dict, List, Set, Tuple

from tarjan import tarjan
from tarjan.tc import tc

from tgen.common.util.dict_util import DictUtil
from tgen.data.dataframes.trace_dataframe import TraceDataFrame
from tgen.data.keys.structure_keys import TraceKeys
from tgen.pipeline.abstract_pipeline_step import AbstractPipelineStep
from tgen.summarizer.artifact.artifacts_summarizer import ArtifactsSummarizer
from tgen.summarizer.summarizer_args import SummarizerArgs
from tgen.summarizer.summarizer_state import SummarizerState
from tgen.summarizer.summarizer_util import SummarizerUtil
from tgen.tracing.ranking.common.ranking_util import RankingUtil


class StepSummarizeArtifacts(AbstractPipelineStep[SummarizerArgs, SummarizerState]):

    def _run(self, args: SummarizerArgs, state: SummarizerState) -> None:
        """
        Summarizes the artifacts for initial run.
        :param args: Arguments to summarizer pipeline.
        :param state: Current state of the summarizer pipeline.
        :return: None
        """
        params = SummarizerUtil.get_params_for_artifact_summarizer(args)
        if args.use_context_in_code_summaries and state.dataset.trace_dataset is not None:
            context_mapping = state.dataset.trace_dataset.create_dependency_mapping()
            summary_order = self.get_summary_order(trace_df=state.dataset.trace_dataset.trace_df)
            DictUtil.update_kwarg_values(params, context_mapping=context_mapping, summary_order=summary_order)
        re_summarize = not SummarizerUtil.needs_project_summary(state.dataset.project_summary, args) and args.do_resummarize_artifacts
        project_summary = state.dataset.project_summary if re_summarize else None
        summarizer = ArtifactsSummarizer(**params, project_summary=project_summary, summarizer_id="First Summary")
        state.dataset.artifact_df.summarize_content(summarizer, re_summarize=re_summarize)
        state.dataset.update_artifact_df(state.dataset.artifact_df)

    @staticmethod
    def get_summary_order(trace_df: TraceDataFrame) -> Dict[str, int]:
        """
        Gets the order that the summaries must occur in by mapping each artifact id to the order it must be summarized in.
        :param trace_df: Contains the trace links for the project.
        :return: Mapping of each artifact id to the order it must be summarized in.
        """
        parent2children = {}
        artifact_ids = set()
        for trace in trace_df.get_links(true_only=True):
            child = trace[TraceKeys.child_label()]
            parent = trace[TraceKeys.parent_label()]
            if parent not in parent2children:
                parent2children[parent] = []
            parent2children[parent].append(child)
            artifact_ids.update({parent, child})

        for a_id in artifact_ids:
            if a_id not in parent2children:
                parent2children[a_id] = []

        tc_output = tc(parent2children)  # 'SpecObject/SpecObject.ss'
        tc_order = tarjan(parent2children)
        artifact2deps = {k: set(v) for k, v in tc_output.items()}
        order = {}
        i = 0
        while len(artifact2deps) > 0:
            next_in_batch = set([k for k, v in artifact2deps.items() if len(v) == 0])
            if len(next_in_batch) == 0:
                next_in_batch = tc_order[0]
            order.update({a_id: i for a_id in next_in_batch})
            artifact2deps = {k: v.difference(next_in_batch) for k, v in artifact2deps.items() if k not in next_in_batch}
            tc_order = [[a_id for a_id in a_batch if a_id not in next_in_batch] for a_batch in tc_order]
            tc_order = [a_batch for a_batch in tc_order if len(a_batch) > 0]
            i += 1
        return order

    @staticmethod
    def find_leaves(links: List[Trace], possible_artifacts: Set[str]) -> Tuple[Set[str], List[Trace]]:
        """
        Finds any leaves within the given artifacts using the given links.
        :param links: All links making up the current tree.
        :param possible_artifacts: All possible artifacts to find leaves in.
        :return: Any leaves within the given artifacts and all links, excluding the leaves.
        """
        parents2links = RankingUtil.group_trace_predictions(links, key_id=TraceKeys.parent_label())
        parent_ids = set(parents2links.keys())
        leaves = possible_artifacts.difference(parent_ids)
        remaining_links = [link for link in links if link[TraceKeys.SOURCE] not in leaves]
        possible_artifacts.difference_update(leaves)
        return leaves, remaining_links

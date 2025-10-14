from trace import Trace
from typing import Dict, List, Set, Tuple

from gen_common.data.dataframes.trace_dataframe import TraceDataFrame
from gen_common.data.keys.structure_keys import TraceKeys
from gen_common.pipeline.abstract_pipeline_step import AbstractPipelineStep
from gen_common.summarize.artifact.artifacts_summarizer import ArtifactsSummarizer
from gen_common.summarize.summarizer_args import SummarizerArgs
from gen_common.summarize.summarizer_state import SummarizerState
from gen_common.summarize.summarizer_util import SummarizerUtil
from gen_common.util.dict_util import DictUtil
from gen_common.util.ranking_util import RankingUtil


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
        possible_links = trace_df.get_links(true_only=True)
        max_depth = len(possible_links)
        remaining_artifacts = trace_df.get_artifact_ids(linked_only=True)
        order = {}
        for d in range(max_depth):
            leaves, possible_links = StepSummarizeArtifacts.find_leaves(possible_links, remaining_artifacts)
            if not leaves:
                break
            for leaf in leaves:
                order[leaf] = d
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

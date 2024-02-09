from trace import Trace
from typing import List, Dict, Set, Tuple

from tgen.common.util.dict_util import DictUtil
from tgen.common.util.enum_util import EnumDict
from tgen.data.dataframes.trace_dataframe import TraceDataFrame
from tgen.data.keys.structure_keys import TraceKeys
from tgen.data.tdatasets.trace_dataset import TraceDataset
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
            context_mapping = self.get_context_mapping(trace_dataset=state.dataset.trace_dataset)
            summary_order = self.get_summary_order(trace_df=state.dataset.trace_dataset.trace_df)
            DictUtil.update_kwarg_values(params, context_mapping=context_mapping, summary_order=summary_order)
        re_summarize = not SummarizerUtil.needs_project_summary(state.dataset.project_summary, args)
        project_summary = state.dataset.project_summary if re_summarize else None
        summarizer = ArtifactsSummarizer(**params, project_summary=project_summary, summarizer_id="First Summary")
        state.dataset.artifact_df.summarize_content(summarizer, re_summarize=re_summarize)
        state.dataset.update_artifact_df(state.dataset.artifact_df)

    @staticmethod
    def get_context_mapping(trace_dataset: TraceDataset) -> Dict[str, List[EnumDict]]:
        """
        Gets the context mapping for the summaries by mapping artifact id to the list of artifacts its dependent on.
        :param trace_dataset: The dataset containing artifacts and traces.
        :return: Mapping of artifact id to the list of artifacts its dependent on.
        """
        artifact_df, trace_df = trace_dataset.artifact_df, trace_dataset.trace_df
        dependencies = {p_id: [link[TraceKeys.child_label()] for link in links]
                        for p_id, links in RankingUtil.group_trace_predictions(trace_df.get_links(true_only=True),
                                                                               key_id=TraceKeys.parent_label()).items()}
        return {p_id: [artifact_df.get_artifact(a_id) for a_id in children] for p_id, children in dependencies.items()}

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
        leaves = possible_artifacts.difference(set(parents2links.keys()))
        remaining_links = [link for link in links if link[TraceKeys.SOURCE] not in leaves]
        possible_artifacts.difference_update(leaves)
        return leaves, remaining_links

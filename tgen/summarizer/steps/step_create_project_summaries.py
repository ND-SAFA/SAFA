from tgen.common.constants.deliminator_constants import EMPTY_STRING
from tgen.common.util.dataclass_util import DataclassUtil
from tgen.common.util.file_util import FileUtil
from tgen.data.tdatasets.prompt_dataset import PromptDataset
from tgen.pipeline.abstract_pipeline_step import AbstractPipelineStep
from tgen.summarizer.project.project_summarizer import ProjectSummarizer
from tgen.summarizer.summarizer_args import SummarizerArgs
from tgen.summarizer.summarizer_state import SummarizerState


class StepCreateProjectSummaries(AbstractPipelineStep[SummarizerArgs, SummarizerState]):

    def _run(self, args: SummarizerArgs, state: SummarizerState) -> None:
        """
        Creates a project summary for each cluster.
        :param args: Arguments to summarizer pipeline.
        :param state: Current state of the summarizer pipeline.
        :return: None
        """
        project_summaries = []
        base_export_dir = args.export_dir.replace(args.summary_dirname, EMPTY_STRING) if args.export_dir else EMPTY_STRING
        for cluster_id, cluster in state.cluster_map.items():
            params = DataclassUtil.convert_to_dict(args, export_dir=FileUtil.safely_join_paths(base_export_dir, cluster_id))
            args_for_cluster = SummarizerArgs(**params)
            dataset = PromptDataset(artifact_df=state.dataset.artifact_df.filter_by_index(cluster.artifact_ids),
                                    project_summary=state.dataset.project_summary)
            ps = ProjectSummarizer(args_for_cluster, dataset=dataset, reload_existing=True).summarize()
            project_summaries.append(ps)
        state.project_summaries = project_summaries

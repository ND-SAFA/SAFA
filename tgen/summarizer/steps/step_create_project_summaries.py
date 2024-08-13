from common_resources.tools.t_logging.logger_manager import logger
from common_resources.tools.util.dataclass_util import DataclassUtil
from common_resources.tools.util.file_util import FileUtil
from common_resources.data.tdatasets.prompt_dataset import PromptDataset
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
        for cluster_id, cluster_artifacts in state.batch_id_to_artifacts.items():
            logger.log_title(f"Creating project summary for {len(cluster_artifacts)} artifacts.")
            export_dir = FileUtil.safely_join_paths(args.export_dir, cluster_id)
            params = DataclassUtil.convert_to_dict(args)
            args_for_cluster = SummarizerArgs(**params)
            args_for_cluster.export_dir = export_dir
            dataset = PromptDataset(artifact_df=state.dataset.artifact_df.filter_by_index(cluster_artifacts),
                                    project_summary=state.dataset.project_summary)
            summarizer = ProjectSummarizer(args_for_cluster, dataset=dataset, reload_existing=True,
                                           summarizer_id=f"Batch {cluster_id} PS")
            ps = summarizer.summarize()
            project_summaries.append(ps)
        state.project_summaries = project_summaries

from tgen.common.util.logging.logger_manager import logger
from tgen.data.tdatasets.prompt_dataset import PromptDataset
from tgen.state.pipeline.abstract_pipeline import AbstractPipelineStep
from tgen.summarizer.project_summarizer import ProjectSummarizer
from tgen.summarizer.summarizer_args import SummarizerArgs
from tgen.tracing.ranking.ranking_args import RankingArgs
from tgen.tracing.ranking.ranking_state import RankingState


class CreateProjectSummary(AbstractPipelineStep[RankingArgs, RankingState]):

    def _run(self, args: RankingArgs, state: RankingState) -> None:
        """
        Sets the pipeline to either NO SUMMARY, MANUAL SUMMARY, or GENERATED SUMMARY.
        If NO SUMMARY, summary is set to None
        If MANUAL SUMMARY then summary is set to given
        If GENERATED SUMMARY then project summary is generated for all artifacts.
        :param args: The pipeline arguments.
        :param state: The state of the pipeline.
        :return: None
        """

        if state.project_summary:
            summary = state.project_summary
        elif args.project_summary is not None and len(args.project_summary) > 0:  # MANUAL SUMMARY
            logger.info("Project summary included in original request.")
            summary = args.project_summary
        elif not args.generate_summary:  # NO SUMMARY
            logger.info("Skipping project summary.")
            summary = None
        else:  # GENERATED SUMMARY
            summarizer = ProjectSummarizer(SummarizerArgs(dataset=PromptDataset(artifact_df=args.artifact_df),
                                                          llm_manager_for_project_summary=args.llm_manager,
                                                          summarize_artifacts=False),
                                           n_tokens=args.n_summary_tokens)
            summary = summarizer.summarize()
        state.project_summary = summary

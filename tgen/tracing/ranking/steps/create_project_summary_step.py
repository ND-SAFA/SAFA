from tgen.common.util.logging.logger_manager import logger
from tgen.state.pipeline.abstract_pipeline import AbstractPipelineStep
from tgen.summarizer.projects.project_summarizer import ProjectSummarizer
from tgen.summarizer.summarizer_args import SummarizerArgs
from tgen.tracing.ranking.ranking_args import RankingArgs
from tgen.tracing.ranking.ranking_state import RankingState


class CreateProjectSummaryStep(AbstractPipelineStep[RankingArgs, RankingState]):

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
        elif args.dataset.project_summary is not None and len(args.dataset.project_summary) > 0:  # MANUAL SUMMARY
            logger.info("Project summary included in dataset.")
            summary = args.dataset.project_summary
        elif not args.generate_summary:  # NO SUMMARY
            logger.info("Skipping project summary.")
            summary = None
        else:  # GENERATED SUMMARY
            summarizer = ProjectSummarizer(SummarizerArgs(dataset=args.dataset,
                                                          llm_manager_for_project_summary=args.llm_manager,
                                                          summarize_artifacts=False,
                                                          export_dir=args.export_dir))
            summary = summarizer.summarize()
        state.project_summary = summary

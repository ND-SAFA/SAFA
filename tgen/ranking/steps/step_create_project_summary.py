import os.path

from tgen.common.util.logging.logger_manager import logger
from tgen.jobs.summary_jobs.project_summary_job import ProjectSummaryJob, ProjectSummaryResponse
from tgen.ranking.ranking_args import RankingArgs
from tgen.ranking.ranking_state import RankingState
from tgen.state.pipeline.abstract_pipeline import AbstractPipelineStep


class CreateProjectSummary(AbstractPipelineStep[RankingArgs, RankingState]):
    def run(self, args: RankingArgs, state: RankingState) -> None:
        """
        Sets the pipeline to either NO SUMMARY, MANUAL SUMMARY, or GENERATED SUMMARY.
        If NO SUMMARY, summary is set to None
        If MANUAL SUMMARY then summary is set to given
        If GENERATED SUMMARY then project summary is generated for all artifacts.
        :param args: The pipeline arguments.
        :param state: The state of the pipeline.
        :return: None
        """
        PROJECT_SUMMARY_FILE_NAME = f"project_summary.yaml"
        PROJECT_SUMMARY_PATH = args.get_path(PROJECT_SUMMARY_FILE_NAME)

        if PROJECT_SUMMARY_PATH is not None and os.path.exists(PROJECT_SUMMARY_PATH):
            summary = args.load(PROJECT_SUMMARY_FILE_NAME)
        elif args.project_summary is not None and len(args.project_summary) > 0:  # MANUAL SUMMARY
            logger.info("Project summary included in original request.")
            summary = args.project_summary
        elif not args.generate_summary:  # NO SUMMARY
            logger.info("Skipping project summary.")
            summary = None
        else:  # GENERATED SUMMARY
            summary_job = ProjectSummaryJob(artifact_map=args.artifact_map, n_tokens=args.n_summary_tokens)
            response: ProjectSummaryResponse = summary_job.run().body
            summary = response["summary"]
            args.save(summary, PROJECT_SUMMARY_FILE_NAME)
        state.project_summary = summary

from tgen.common.util.logging.logger_manager import logger
from tgen.common.util.status import Status
from tgen.data.dataframes.artifact_dataframe import ArtifactKeys
from tgen.delta.delta_args import DeltaArgs
from tgen.delta.delta_state import DeltaState
from tgen.jobs.summary_jobs.project_summary_job import ProjectSummaryJob, ProjectSummaryResponse
from tgen.state.pipeline.abstract_pipeline import AbstractPipelineStep


class ProjectSummaryStep(AbstractPipelineStep[DeltaArgs, DeltaState]):

    def run(self, args: DeltaArgs, state: DeltaState) -> None:
        """
        Gets the summary of the project
        :param args: The delta summarizer args
        :param state:  The delta summarizer state
        :return: None
        """
        if state.project_summary:
            return
        logger.log_with_title("STEP 1 - Generating Project Summary")
        original_artifacts = args.dataset.artifact_df
        summary_job = ProjectSummaryJob({a_id: original_artifacts.get_artifact(a_id)[ArtifactKeys.CONTENT]
                                         for a_id in original_artifacts.index})
        job_res = summary_job.run()
        assert job_res.status == Status.SUCCESS, "Project summary job failed"
        summary_res: ProjectSummaryResponse = job_res.body
        state.project_summary = summary_res["summary"]
        state.on_step_complete(self.__class__.__name__)

from api.endpoints.base.views.endpoint import async_endpoint
from api.endpoints.project_summary.project_summary_serializer import ProjectSummaryRequest, \
    ProjectSummarySerializer
from tgen.common.util.status import Status
from tgen.jobs.summary_jobs.project_summary_job import ProjectSummaryJob, ProjectSummaryResponse


@async_endpoint(ProjectSummarySerializer)
def perform_project_summary(request_data: ProjectSummaryRequest) -> ProjectSummaryResponse:
    """
    Creates a project specification summarizing artifacts in system.
    :param request_data: The summary request containing artifacts.
    :return: Project summary as string
    """
    artifact_map = request_data["artifacts"]
    job = ProjectSummaryJob(artifact_map=artifact_map)
    job_result = job.run()
    if job_result.status == Status.FAILURE:
        raise Exception(job_result.body)
    project_summary: ProjectSummaryResponse = job_result.body
    return project_summary

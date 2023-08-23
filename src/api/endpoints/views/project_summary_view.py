from api.endpoints.base.endpoint import async_endpoint
from api.endpoints.serializers.project_summary_serializer import ProjectSummaryRequest, \
    ProjectSummarySerializer
from tgen.common.util.status import Status
from tgen.jobs.summary_jobs.project_summary_job import ProjectSummaryJob
from tgen.jobs.summary_jobs.summary_response import SummaryResponse

LAYER_ID = "LAYER_ID"


@async_endpoint(ProjectSummarySerializer)
def perform_project_summary(request_data: ProjectSummaryRequest) -> SummaryResponse:
    """
    Creates a project specification summarizing artifacts in system.
    :param request_data: The summary request containing artifacts.
    :return: Project summary as string
    """
    artifacts = request_data["artifacts"]
    job = ProjectSummaryJob(artifacts=artifacts)
    job_result = job.run()
    if job_result.status == Status.FAILURE:
        raise Exception(job_result.body)
    project_summary: SummaryResponse = job_result.body
    return project_summary

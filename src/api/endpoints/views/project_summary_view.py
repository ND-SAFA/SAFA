from api.endpoints.base.endpoint import async_endpoint
from api.endpoints.serializers.project_summary_serializer import ProjectSummaryRequest, \
    ProjectSummarySerializer
from tgen.common.util.enum_util import EnumDict
from tgen.common.util.status import Status
from tgen.data.dataframes.artifact_dataframe import ArtifactKeys
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
    artifact_map = request_data["artifacts"]

    artifacts = [
        EnumDict({
            ArtifactKeys.ID: a_id,
            ArtifactKeys.CONTENT: a_body,
            ArtifactKeys.LAYER_ID: LAYER_ID
        }) for a_id, a_body in artifact_map.items()
    ]
    job = ProjectSummaryJob(artifacts=artifacts)
    job_result = job.run()
    if job_result.status == Status.FAILURE:
        raise Exception(job_result.body)
    project_summary: SummaryResponse = job_result.body
    return project_summary

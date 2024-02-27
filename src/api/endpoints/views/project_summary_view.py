from api.endpoints.common.dataset_converter import create_api_dataset
from api.endpoints.common.endpoint_decorator import endpoint
from api.endpoints.serializers.project_summary_serializer import ProjectSummaryRequest, \
    ProjectSummarySerializer
from tgen.common.util.status import Status
from tgen.jobs.summary_jobs.summarize_job import SummarizeJob
from tgen.jobs.summary_jobs.summary_response import SummaryResponse

LAYER_ID = "LAYER_ID"


@endpoint(ProjectSummarySerializer, is_async=True)
def perform_project_summary(request_data: ProjectSummaryRequest) -> SummaryResponse:
    """
    Creates a project specification summarizing artifacts in system.
    :param request_data: The summary request containing artifacts.
    :return: Project summary as string
    """
    artifacts = request_data["artifacts"]
    kwargs = request_data.get("kwargs", {})
    dataset_creator = create_api_dataset(artifacts)
    job = SummarizeJob(dataset_creator=dataset_creator, **kwargs)
    job_result = job.run()
    if job_result.status == Status.FAILURE:
        raise Exception(job_result.body)
    summary_response: SummaryResponse = job_result.body
    return summary_response

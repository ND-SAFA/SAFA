from api.endpoints.gen.health.health_check_serializer import HealthCheckRequest, HealthCheckSerializer
from api.endpoints.handler.endpoint_decorator import endpoint
from api.utils.view_util import ViewUtil
from tgen.jobs.health_check_jobs.health_check_job import HealthCheckJob
from tgen.jobs.health_check_jobs.health_check_results import HealthCheckResults


@endpoint(HealthCheckSerializer, is_async=True)
def perform_health_check(request: HealthCheckRequest) -> HealthCheckResults:
    """
    Performs a health check on a given artifact.
    :param request: The request containing a dataset for context and the id of the artifact to perform health check on.
    :return: The results of the health check.
    """
    job_args = ViewUtil.create_job_args_from_api_definition(request.dataset)
    job = HealthCheckJob(job_args, query_ids=request.query_ids, concept_layer_id=request.concept_layer_id)
    health_check_results = ViewUtil.run_job(job)
    return health_check_results

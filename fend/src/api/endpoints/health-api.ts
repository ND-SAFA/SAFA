import { JobSchema } from "@/types";
import { projectStore } from "@/hooks";
import { buildRequest } from "@/api";
import { HealthRequest, HealthTask } from "@/types/api/health-api";

/**
 * Performs health checks on artifacts.
 * @param tasks The tasks to perform on artifacts.
 * @param artifactIds The ids of the artifacts.
 * @param artifactTypes Types to perform on.
 */
export function performHealthChecks(
  tasks: HealthTask[],
  artifactIds: string[],
  artifactTypes: string[]
): Promise<JobSchema> {
  const versionId = projectStore.versionId;
  const request: HealthRequest = {
    versionId,
    tasks,
    artifactIds,
    artifactTypes,
  };
  return buildRequest<JobSchema, "", HealthRequest>("healthChecks").post(
    request
  );
}

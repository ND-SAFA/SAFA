import { Artifact, ProjectCreationResponse, TraceLink } from "@/types";
import { Endpoint, fillEndpoint, authHttpClient } from "@/api/util";

/**
 * Gets a specific version of a project.
 *
 * @param versionId - The project version ID to get.
 *
 * @return The matching project.
 */
export async function getProjectVersion(
  versionId: string
): Promise<ProjectCreationResponse> {
  return authHttpClient<ProjectCreationResponse>(
    fillEndpoint(Endpoint.projectVersion, { versionId }),
    { method: "GET" }
  );
}

/**
 * Returns the current list of artifacts present in given version.
 * @param versionId The id of the version whose artifacts are returned.
 *
 * @return Promise returning list of artifacts in given version.
 */
export async function getArtifactsInVersion(
  versionId: string
): Promise<Artifact[]> {
  return authHttpClient<Artifact[]>(
    fillEndpoint(Endpoint.getArtifactsInVersion, { versionId }),
    { method: "GET" }
  );
}

/**
 * Returns the current list of traces in specified version.
 * @param versionId The version id whose traces are being returned.
 * @return list of traces in version
 */
export async function getTracesInVersion(
  versionId: string
): Promise<TraceLink[]> {
  return authHttpClient<TraceLink[]>(
    fillEndpoint(Endpoint.getTracesInVersion, { versionId }),
    { method: "GET" }
  );
}

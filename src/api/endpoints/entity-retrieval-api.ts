import { Artifact, ProjectEntities, TraceLink } from "@/types";
import { Endpoint, fillEndpoint, authHttpClient } from "@/api/util";

/**
 * Gets a specific version of a project.
 *
 * @param versionId - The project version ID to get.
 * @return The matching project.
 */
export async function getProjectVersion(
  versionId: string
): Promise<ProjectEntities> {
  return authHttpClient<ProjectEntities>(
    fillEndpoint(Endpoint.projectVersion, { versionId }),
    { method: "GET" }
  );
}

/**
 * Returns the list of artifacts in the given version.
 *
 * @param versionId - The version whose artifacts are returned.
 * @return The list of artifacts.
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
 * Returns the list of trace links in the given version.
 *
 * @param versionId - The version whose trace links are returned.
 * @return The list of trace links.
 */
export async function getTracesInVersion(
  versionId: string
): Promise<TraceLink[]> {
  return authHttpClient<TraceLink[]>(
    fillEndpoint(Endpoint.getTracesInVersion, { versionId }),
    { method: "GET" }
  );
}

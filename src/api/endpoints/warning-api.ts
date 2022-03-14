import { Project, ProjectWarnings } from "@/types";
import { authHttpClient, Endpoint, fillEndpoint } from "@/api";

/**
 * Returns the project warnings in the given project version.
 * @param versionId The version id whose warnings are returned.
 */
export async function getWarningsInProjectVersion(
  versionId: string
): Promise<ProjectWarnings> {
  const endpoint = fillEndpoint(Endpoint.getWarningsInProjectVersion, {
    versionId,
  });
  return authHttpClient<ProjectWarnings>(endpoint, {
    method: "GET",
  });
}

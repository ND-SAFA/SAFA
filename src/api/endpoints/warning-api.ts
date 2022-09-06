import { ProjectWarnings } from "@/types";
import { authHttpClient, Endpoint, fillEndpoint } from "@/api";

/**
 * Returns the project warnings in the given project version.
 *
 * @param versionId The version id whose warnings are returned.
 * @return The project warnings.
 */
export async function getWarningsInProjectVersion(
  versionId: string
): Promise<ProjectWarnings> {
  return authHttpClient<ProjectWarnings>(
    fillEndpoint(Endpoint.getWarningsInProjectVersion, {
      versionId,
    }),
    {
      method: "GET",
    }
  );
}

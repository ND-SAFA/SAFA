import { authHttpClient, Endpoint, fillEndpoint } from "@/api";
import { ArtifactPositions } from "@/types";

/**
 * Returns a mapping of artifact names to their position.
 * @param versionId ID of version of the project to layout.
 */
export async function getProjectLayout(
  versionId: string
): Promise<ArtifactPositions> {
  // TODO: remove
  try {
    return await authHttpClient<ArtifactPositions>(
      fillEndpoint(Endpoint.getProjectLayout, {
        versionId,
      }),
      {
        method: "POST",
      }
    );
  } catch (e) {
    return {};
  }
}

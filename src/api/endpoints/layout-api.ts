import { authHttpClient, Endpoint, fillEndpoint } from "@/api";

export interface Position {
  /**
   * Number of pixels left from top left corner of parent container.
   */
  x: number;
  /**
   * Number of pixels down from top left corner of parent container.
   */
  y: number;
}

type ArtifactPositions = Record<string, Position>;

/**
 * Returns a mapping of artifact names to their position.
 * @param versionId ID of version of the project to layout.
 */
export async function getProjectLayout(
  versionId: string
): Promise<ArtifactPositions> {
  return authHttpClient<ArtifactPositions>(
    fillEndpoint(Endpoint.getProjectLayout, {
      versionId,
    }),
    {
      method: "POST",
    }
  );
}

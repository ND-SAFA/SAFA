import { Artifact, ArtifactDeltaState } from "@/types";
import { ThemeColors } from "@/util/theme";

/**
 * Returns the artifact in list if single item exists.
 *
 * @param query - List of artifacts representing some query for an artifact.
 * @param queryName - The name of the operation to log if operation fails.
 * @return The found artifact.
 * @throws Error if query contains multiple or no results.
 */
export function getSingleQueryResult(
  query: Artifact[],
  queryName: string
): Artifact {
  switch (query.length) {
    case 1:
      return query[0];
    case 0:
      throw Error(`Query resulted in empty results: ${queryName}`);
    default:
      throw Error(`Found more than one result in query: ${queryName}`);
  }
}

/**
 * Returns the background color for the given delta state.
 * @param deltaState - The delta state to get the color for.
 * @return The color.
 */
export function getBackgroundColor(deltaState?: ArtifactDeltaState): string {
  switch (deltaState) {
    case ArtifactDeltaState.ADDED:
      return ThemeColors.artifactAdded;
    case ArtifactDeltaState.REMOVED:
      return ThemeColors.artifactRemoved;
    case ArtifactDeltaState.MODIFIED:
      return ThemeColors.artifactModified;
    default:
      return ThemeColors.artifactDefault;
  }
}

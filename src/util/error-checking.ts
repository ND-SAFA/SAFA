import { Artifact } from "@/types";
import { appModule } from "@/store";

/**
 * Returns the artifact in list if single item exists.
 * @throws Error if query contains no or multiple results.
 * @param query List of artifacts representing some query for an artifact.
 * @param queryName The name of the operation to log if operation fails.
 */
export function getSingleQueryResult(
  query: Artifact[],
  queryName: string
): Artifact {
  if (query.length === 0) {
    const error = `Query resulted in empty results: ${queryName}`;
    appModule.onWarning(error);
    throw Error(error);
  } else if (query.length > 1) {
    const error = `Found more than one result in query: ${queryName}`;
    appModule.onWarning(error);
    throw Error(error);
  } else {
    return query[0];
  }
}

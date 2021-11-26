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
  let error;
  switch (query.length) {
    case 1:
      return query[0];
    case 0:
      error = `Query resulted in empty results: ${queryName}`;
      appModule.onWarning(error);
      throw Error(error);
    default:
      error = `Found more than one result in query: ${queryName}`;
      appModule.onWarning(error);
      throw Error(error);
  }
}

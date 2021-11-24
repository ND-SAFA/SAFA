import { Artifact } from "@/types";
import { appModule } from "@/store";

/**
 * Returns the only result in query and throws error if fails.
 * @throws Error if query contains no results or more than a single result.
 * @param query
 * @param queryName
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

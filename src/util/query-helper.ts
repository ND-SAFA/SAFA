/**
 * Returns the artifact in list if single item exists.
 *
 * @param query - List of artifacts representing some query for an artifact.
 * @param queryName - The name of the operation to log if operation fails.
 * @return The found artifact.
 * @throws Error if query contains multiple or no results.
 */
export function getSingleQueryResult<Entity>(
  query: Entity[],
  queryName: string
): Entity {
  switch (query.length) {
    case 1:
      return query[0];
    case 0:
      throw Error(`Query resulted in empty results: ${queryName}`);
    default:
      throw Error(`Found more than one result in query: ${queryName}`);
  }
}

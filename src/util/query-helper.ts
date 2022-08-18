/**
 * Returns the artifact in list if single item exists.
 *
 * @param query - List of artifacts representing some query for an artifact.
 * @return The found object.
 */
export function getSingleQueryResult<Entity>(
  query: Entity[]
): Entity | undefined {
  return query.length === 1 ? query[0] : undefined;
}

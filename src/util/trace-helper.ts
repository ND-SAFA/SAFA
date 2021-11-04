/**
 * Returns the trace ID made from the given source and target IDs.
 *
 * @param source - The source ID.
 * @param target - THe target ID.
 *
 * @return The standardized ID of the source joined to the target.
 */
export function getTraceId(source: string, target: string): string {
  return `${source}-${target}`;
}

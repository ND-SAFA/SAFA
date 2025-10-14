import { buildRequest } from "@/api";

/**
 * Persists trace matrices between given source and target
 * artifact types in given project.
 *
 * @param versionId - The project version whose trace matrix will be stored.
 * @param sourceType - The source artifact type name.
 * @param targetType - The target artifact type name.
 */
export async function createTraceMatrix(
  versionId: string,
  sourceType: string,
  targetType: string
): Promise<void> {
  return buildRequest<void, "versionId" | "sourceType" | "targetType">(
    "traceMatrix",
    { versionId, sourceType, targetType }
  ).post();
}

/**
 * Deletes the trace matrix between the given source and target artifact types.
 *
 * @param versionId - The project version to delete this trace matrix within.
 * @param sourceType - The source artifact type name.
 * @param targetType - The target artifact type name.
 */
export async function deleteTraceMatrix(
  versionId: string,
  sourceType: string,
  targetType: string
): Promise<void> {
  return buildRequest<void, "versionId" | "sourceType" | "targetType">(
    "traceMatrix",
    { versionId, sourceType, targetType }
  ).delete();
}

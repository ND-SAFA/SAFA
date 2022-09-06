import { ArtifactTypeDirections } from "@/types";
import { authHttpClient, Endpoint, fillEndpoint } from "@/api";

/**
 * Persists trace matrices between given source and target
 * artifact types in given project.
 *
 * @param projectId - The project whose trace matrix will be stored.
 * @param sourceType - The source artifact type name.
 * @param targetType - The target artifact type name.
 */
export async function createTraceMatrix(
  projectId: string,
  sourceType: string,
  targetType: string
): Promise<void> {
  return authHttpClient<void>(
    fillEndpoint(Endpoint.createTraceMatrix, {
      projectId,
      sourceType,
      targetType,
    }),
    {
      method: "POST",
    }
  );
}

/**
 * Returns the trace directions allowed in given project.
 *
 * @param projectId - The project to load from.
 * @return The loaded trace matrices.
 */
export async function getTraceMatrices(
  projectId: string
): Promise<ArtifactTypeDirections> {
  return authHttpClient<ArtifactTypeDirections>(
    fillEndpoint(Endpoint.retrieveTraceMatrices, {
      projectId,
    }),
    {
      method: "GET",
    }
  );
}

/**
 * Deletes the trace matrix between the given source and target artifact types.
 *
 * @param projectId - The project to delete this trace matrix within.
 * @param sourceType - The source artifact type name.
 * @param targetType - The target artifact type name.
 */
export async function deleteTraceMatrix(
  projectId: string,
  sourceType: string,
  targetType: string
): Promise<void> {
  return authHttpClient<void>(
    fillEndpoint(Endpoint.deleteTraceMatrix, {
      projectId,
      sourceType,
      targetType,
    }),
    {
      method: "DELETE",
    }
  );
}

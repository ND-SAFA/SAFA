import { ArtifactTypeDirections, Project } from "@/types";
import { authHttpClient, Endpoint, fillEndpoint } from "@/api";

/**
 * Persists a trace matrices between given source and target
 * artifact types in given project.
 * @param project The project whose trace matrix will be stored with.
 * @param sourceArtifactTypeName The source artifact type name.
 * @param targetArtifactTypeName The target artifact type name.
 */
export async function createTraceMatrix(
  project: Project,
  sourceArtifactTypeName: string,
  targetArtifactTypeName: string
): Promise<void> {
  const url = fillEndpoint(Endpoint.createTraceMatrix, {
    projectId: project.projectId,
    sourceArtifactTypeName,
    targetArtifactTypeName,
  });
  return authHttpClient<void>(url, {
    method: "POST",
  });
}

/**
 * Returns the trace directions allowed in given project.
 * @param project
 */
export async function retrieveTraceMatrices(
  project: Project
): Promise<ArtifactTypeDirections> {
  const url = fillEndpoint(Endpoint.retrieveTraceMatrices, {
    projectId: project.projectId,
  });
  return authHttpClient<ArtifactTypeDirections>(url, {
    method: "GET",
  });
}

/**
 * Deletes TraceMatrix between given source and target artifact types
 * within specified project.
 * @param project
 * @param sourceArtifactTypeName
 * @param targetArtifactTypeName
 */
export async function deleteTraceMatrix(
  project: Project,
  sourceArtifactTypeName: string,
  targetArtifactTypeName: string
): Promise<void> {
  const url = fillEndpoint(Endpoint.deleteTraceMatrix, {
    projectId: project.projectId,
    sourceArtifactTypeName,
    targetArtifactTypeName,
  });
  return authHttpClient<void>(url, {
    method: "DELETE",
  });
}

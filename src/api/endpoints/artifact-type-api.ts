import { ArtifactType, Project, ProjectDocument } from "@/types";
import { authHttpClient, Endpoint, fillEndpoint } from "@/api";

/**
 * Creates artifact type if typeId is null otherwise updates the entity.
 * @param projectId The project whose the type will be created for.
 * @param artifactType The artifact type to create or update.
 */
export async function createOrUpdateArtifactType(
  projectId: string,
  artifactType: ArtifactType
): Promise<ArtifactType> {
  const url = fillEndpoint(Endpoint.createOrUpdateArtifactType, {
    projectId,
  });
  return authHttpClient<ArtifactType>(url, {
    method: "POST",
    body: JSON.stringify(artifactType),
  });
}

/**
 * Deletes the artifact with given id.
 * @param typeId
 */
export async function deleteArtifactType(typeId: string): Promise<void> {
  const url = fillEndpoint(Endpoint.deleteArtifactType, {
    typeId,
  });
  return authHttpClient<void>(url, {
    method: "DELETE",
  });
}

/**
 * Returns the list of artifact types associated with project specified.
 * @param projectId The id of the project whose types are returned.
 */
export async function getProjectArtifactTypes(
  projectId: string
): Promise<ArtifactType[]> {
  const url = fillEndpoint(Endpoint.getProjectArtifactTypes, {
    projectId,
  });
  return authHttpClient<ArtifactType[]>(url, {
    method: "GET",
  });
}

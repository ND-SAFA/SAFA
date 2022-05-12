import { ArtifactType } from "@/types";
import { authHttpClient, Endpoint, fillEndpoint } from "@/api";

/**
 * Creates artifact type if typeId is null, otherwise updates the entity.
 *
 * @param projectId - The project whose the type will be created for.
 * @param artifactType - The artifact type to create or update.
 * @return The saved artifact type.
 */
export async function saveArtifactType(
  projectId: string,
  artifactType: ArtifactType
): Promise<ArtifactType> {
  return authHttpClient<ArtifactType>(
    fillEndpoint(Endpoint.createOrUpdateArtifactType, {
      projectId,
    }),
    {
      method: "POST",
      body: JSON.stringify(artifactType),
    }
  );
}

/**
 * Deletes the artifact type with given id.
 *
 * @param typeId - The artifact type to delete.
 */
export async function deleteArtifactType(typeId: string): Promise<void> {
  return authHttpClient<void>(
    fillEndpoint(Endpoint.deleteArtifactType, {
      typeId,
    }),
    {
      method: "DELETE",
    }
  );
}

/**
 * Returns the list of artifact types associated with project specified.
 *
 * @param projectId - The id of the project whose types are returned.
 * @return All artifact types.
 */
export async function getProjectArtifactTypes(
  projectId: string
): Promise<ArtifactType[]> {
  return authHttpClient<ArtifactType[]>(
    fillEndpoint(Endpoint.getProjectArtifactTypes, {
      projectId,
    }),
    {
      method: "GET",
    }
  );
}

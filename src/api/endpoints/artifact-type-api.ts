import { ArtifactTypeSchema } from "@/types";
import { authHttpClient, Endpoint, fillEndpoint } from "@/api";

/**
 * Creates a new artifact type.
 *
 * @param projectId - The project who's the type will be created for.
 * @param artifactType - The artifact type to create.
 * @return The saved artifact type.
 */
export async function createArtifactType(
  projectId: string,
  artifactType: ArtifactTypeSchema
): Promise<ArtifactTypeSchema> {
  return authHttpClient<ArtifactTypeSchema>(
    fillEndpoint(Endpoint.createArtifactType, {
      projectId,
    }),
    {
      method: "POST",
      body: JSON.stringify(artifactType),
    }
  );
}

/**
 * Edits an existing artifact type.
 *
 * @param projectId - The project who's the type will be edited for.
 * @param artifactType - The artifact type to update.
 * @return The saved artifact type.
 */
export async function editArtifactType(
  projectId: string,
  artifactType: ArtifactTypeSchema
): Promise<ArtifactTypeSchema> {
  return authHttpClient<ArtifactTypeSchema>(
    fillEndpoint(Endpoint.editArtifactType, {
      projectId,
      artifactTypeName: artifactType.name,
    }),
    {
      method: "PUT",
      body: JSON.stringify(artifactType),
    }
  );
}

/**
 * Deletes the artifact type with given id.
 *
 * @param artifactTypeName - The artifact type to delete.
 */
export async function deleteArtifactType(
  artifactTypeName: string
): Promise<void> {
  return authHttpClient<void>(
    fillEndpoint(Endpoint.deleteArtifactType, {
      artifactTypeName,
    }),
    {
      method: "DELETE",
    }
  );
}

import { ArtifactTypeSchema } from "@/types";
import { authHttpClient, Endpoint, fillEndpoint } from "@/api";

/**
 * Creates artifact type if typeId is null, otherwise updates the entity.
 *
 * @param projectId - The project who's the type will be created for.
 * @param artifactType - The artifact type to create or update.
 * @return The saved artifact type.
 */
export async function saveArtifactType(
  projectId: string,
  artifactType: ArtifactTypeSchema
): Promise<ArtifactTypeSchema> {
  return authHttpClient<ArtifactTypeSchema>(
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

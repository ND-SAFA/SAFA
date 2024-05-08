import { ArtifactTypeSchema } from "@/types";
import { buildRequest } from "@/api";

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
  return buildRequest<ArtifactTypeSchema, "projectId", ArtifactTypeSchema>(
    "artifactTypeCollection",
    { projectId }
  ).post(artifactType);
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
  return buildRequest<
    ArtifactTypeSchema,
    "projectId" | "artifactTypeName",
    ArtifactTypeSchema
  >("artifactType", { projectId, artifactTypeName: artifactType.name }).put(
    artifactType
  );
}

/**
 * Deletes the artifact type with given id.
 *
 * @param projectId - The project who's the type will be deleted from.
 * @param artifactTypeName - The artifact type to delete.
 */
export async function deleteArtifactType(
  projectId: string,
  artifactTypeName: string
): Promise<void> {
  return buildRequest<void, "projectId" | "artifactTypeName">("artifactType", {
    projectId,
    artifactTypeName,
  }).delete();
}

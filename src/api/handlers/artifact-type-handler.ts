import { ArtifactType } from "@/types";
import { createOrUpdateArtifactType } from "@/api/endpoints/artifact-type-api";
import { projectModule } from "@/store";

/**
 * Creates or updates the given artifact type.
 *
 * @param artifactType - The artifact type to add or edit.
 */
export async function artifactTypeChangeHandler(
  artifactType: ArtifactType
): Promise<void> {
  const updatedArtifactType = await createOrUpdateArtifactType(
    projectModule.projectId,
    artifactType
  );

  projectModule.addOrUpdateArtifactType(updatedArtifactType);
}

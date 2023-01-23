import { ArtifactTypeSchema, TimArtifactLevelSchema } from "@/types";
import { projectStore, typeOptionsStore } from "@/hooks";
import { saveArtifactType } from "@/api/endpoints";

/**
 * Creates or updates the given artifact type.
 *
 * @param artifactType - The artifact type to add or edit.
 */
export async function handleSaveArtifactType(
  artifactType: ArtifactTypeSchema
): Promise<void> {
  const updatedArtifactType = await saveArtifactType(
    projectStore.projectId,
    artifactType
  );

  typeOptionsStore.addOrUpdateArtifactTypes([updatedArtifactType]);
}

/**
 * Updates the icon for an artifact type.
 *
 * @param artifactLevel - The artifact type to add or edit.
 */
export async function handleSaveArtifactTypeIcon(
  artifactLevel: TimArtifactLevelSchema
): Promise<void> {
  const type = typeOptionsStore.allArtifactTypes.find(
    ({ typeId }) => typeId === artifactLevel.typeId
  );

  if (!type) return;

  typeOptionsStore.updateArtifactIcon(artifactLevel);
  await handleSaveArtifactType({ ...type, icon: artifactLevel.icon });
}

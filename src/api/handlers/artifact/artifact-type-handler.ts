import { ArtifactTypeSchema, LabelledTraceDirectionSchema } from "@/types";
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
 * @param labeledType - The artifact type to add or edit.
 */
export async function handleSaveArtifactTypeIcon(
  labeledType: LabelledTraceDirectionSchema
): Promise<void> {
  const type = typeOptionsStore.allArtifactTypes.find(
    ({ name }) => name === labeledType.type
  );

  if (!type) return;

  typeOptionsStore.updateArtifactIcon(labeledType);
  await handleSaveArtifactType({ ...type, icon: labeledType.icon });
}

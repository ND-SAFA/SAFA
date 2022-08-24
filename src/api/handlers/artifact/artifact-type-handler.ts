import { ArtifactTypeModel, LabelledTraceDirectionModel } from "@/types";
import { saveArtifactType } from "@/api/endpoints";
import { projectStore, typeOptionsStore } from "@/hooks";

/**
 * Creates or updates the given artifact type.
 *
 * @param artifactType - The artifact type to add or edit.
 */
export async function handleSaveArtifactType(
  artifactType: ArtifactTypeModel
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
  labeledType: LabelledTraceDirectionModel
): Promise<void> {
  const type = typeOptionsStore.allArtifactTypes.find(
    ({ name }) => name === labeledType.type
  );

  if (!type) return;

  typeOptionsStore.updateArtifactIcon(labeledType);
  await handleSaveArtifactType({ ...type, icon: labeledType.icon });
}

import { ArtifactTypeModel, LabelledTraceDirectionModel } from "@/types";
import { saveArtifactType } from "@/api/endpoints/artifact-type-api";
import { projectModule } from "@/store";
import { typeOptionsStore } from "@/hooks";

/**
 * Creates or updates the given artifact type.
 *
 * @param artifactType - The artifact type to add or edit.
 */
export async function handleSaveArtifactType(
  artifactType: ArtifactTypeModel
): Promise<void> {
  const updatedArtifactType = await saveArtifactType(
    projectModule.projectId,
    artifactType
  );

  projectModule.addOrUpdateArtifactType(updatedArtifactType);
}

/**
 * Updates the icon for an artifact type.
 *
 * @param labeledType - The artifact type to add or edit.
 */
export async function handleSaveArtifactTypeIcon(
  labeledType: LabelledTraceDirectionModel
): Promise<void> {
  const type = projectModule.getProject.artifactTypes.find(
    ({ name }) => name === labeledType.type
  );

  if (!type) return;

  typeOptionsStore.updateArtifactIcon(labeledType);
  await handleSaveArtifactType({ ...type, icon: labeledType.icon });
}

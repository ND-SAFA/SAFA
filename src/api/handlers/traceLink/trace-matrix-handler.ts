import { typeOptionsStore, projectStore } from "@/hooks";
import { deleteTraceMatrix, getTraceMatrices } from "@/api";
import { LabelledTraceDirectionModel } from "@/types";

/**
 * Updates the trace matrices for the project.
 *
 * @return The current trace matrices.
 */
export async function handleLoadTraceMatrices(): Promise<void> {
  const artifactTypeDirections = await getTraceMatrices(projectStore.projectId);

  typeOptionsStore.$patch({ artifactTypeDirections });
}

/**
 * Removes traces from the given source to target artifact types.
 *
 * @param sourceArtifactTypeName - The source artifact type name.
 * @param targetArtifactTypeName - The target artifact type name.
 */
export async function handleRemoveTraceType(
  sourceArtifactTypeName: string,
  targetArtifactTypeName: string
): Promise<void> {
  await deleteTraceMatrix(
    projectStore.projectId,
    sourceArtifactTypeName,
    targetArtifactTypeName
  );
}

/**
 * Removes a saved artifact type direction and updates related stores.
 *
 * @param labeledType - The artifact type to edit.
 * @param removedType - The type direction to remove.
 */
export async function handleRemoveDirection(
  labeledType: LabelledTraceDirectionModel,
  removedType: string
): Promise<void> {
  labeledType.allowedTypes = labeledType.allowedTypes.filter(
    (allowedType) => allowedType !== removedType
  );

  typeOptionsStore.updateLinkDirections(labeledType);
  await handleRemoveTraceType(labeledType.type, removedType);
}

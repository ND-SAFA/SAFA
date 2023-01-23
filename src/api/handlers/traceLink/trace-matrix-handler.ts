import { TimArtifactLevelSchema } from "@/types";
import { typeOptionsStore, projectStore } from "@/hooks";
import { deleteTraceMatrix, getTraceMatrices } from "@/api";

/**
 * Updates the trace matrices for the project.
 *
 * @return The current trace matrices.
 */
export async function handleLoadTraceMatrices(): Promise<void> {
  typeOptionsStore.initializeTypeDirections(
    await getTraceMatrices(projectStore.projectId)
  );
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
 * @param artifactLevel - The artifact type to edit.
 * @param removedType - The type direction to remove.
 */
export async function handleRemoveDirection(
  artifactLevel: TimArtifactLevelSchema,
  removedType: string
): Promise<void> {
  artifactLevel.allowedTypes = artifactLevel.allowedTypes.filter(
    (allowedType) => allowedType !== removedType
  );

  typeOptionsStore.updateLinkDirections(artifactLevel);
  await handleRemoveTraceType(artifactLevel.name, removedType);
}

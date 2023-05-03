import { TimArtifactLevelSchema } from "@/types";
import { typeOptionsStore, projectStore, logStore } from "@/hooks";
import { createTraceMatrix, deleteTraceMatrix } from "@/api";

/**
 * Creates traces from the given source to target artifact types.
 *
 * @param sourceArtifactTypeName - The source artifact type name.
 * @param targetArtifactTypeName - The target artifact type name.
 */
export async function handleCreateTraceType(
  sourceArtifactTypeName: string,
  targetArtifactTypeName: string
): Promise<void> {
  try {
    await createTraceMatrix(
      projectStore.projectId,
      sourceArtifactTypeName,
      targetArtifactTypeName
    );

    typeOptionsStore.updateLinkDirections({
      name: sourceArtifactTypeName,
      allowedTypes: [
        ...typeOptionsStore.tim.artifacts[sourceArtifactTypeName].allowedTypes,
        targetArtifactTypeName,
      ],
    });

    logStore.onSuccess(
      `Created trace direction: ${sourceArtifactTypeName} -> ${targetArtifactTypeName}`
    );
  } catch (e) {
    logStore.onError(
      `Unable to create trace direction: ${sourceArtifactTypeName} -> ${targetArtifactTypeName}`
    );
  }
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
  try {
    await deleteTraceMatrix(
      projectStore.projectId,
      sourceArtifactTypeName,
      targetArtifactTypeName
    );

    logStore.onSuccess(
      `Deleted trace direction: ${sourceArtifactTypeName} -> ${targetArtifactTypeName}`
    );
  } catch (e) {
    logStore.onError(
      `Unable to delete trace direction: ${sourceArtifactTypeName} -> ${targetArtifactTypeName}`
    );
  }
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

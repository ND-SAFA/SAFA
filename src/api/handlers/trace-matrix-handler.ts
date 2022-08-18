import { projectModule, typeOptionsModule } from "@/store";
import { deleteTraceMatrix, getTraceMatrices } from "@/api";
import { LabelledTraceDirectionModel } from "@/types";

/**
 * Updates the trace matrices for the project.
 *
 * @return The current trace matrices.
 */
export async function handleLoadTraceMatrices(): Promise<void> {
  const matrix = await getTraceMatrices(projectModule.projectId);

  typeOptionsModule.SET_LINK_DIRECTIONS(matrix);
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
    projectModule.projectId,
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

  typeOptionsModule.updateLinkDirections(labeledType);
  await handleRemoveTraceType(labeledType.type, removedType);
}

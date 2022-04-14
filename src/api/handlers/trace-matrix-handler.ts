import { deleteTraceMatrix, getTraceMatrices } from "@/api";
import { projectModule, typeOptionsModule } from "@/store";

/**
 * Updates the trace matrices for the project.
 *
 * @return The current trace matrices.
 */
export async function reloadTraceMatrices(): Promise<void> {
  const matrix = await getTraceMatrices(projectModule.projectId);

  typeOptionsModule.SET_LINK_DIRECTIONS(matrix);
}

/**
 * Removes traces from the given source to target artifact types.
 *
 * @param sourceArtifactTypeName - The source artifact type name.
 * @param targetArtifactTypeName - The target artifact type name.
 */
export async function removeTraceType(
  sourceArtifactTypeName: string,
  targetArtifactTypeName: string
): Promise<void> {
  await deleteTraceMatrix(
    projectModule.projectId,
    sourceArtifactTypeName,
    targetArtifactTypeName
  );
}

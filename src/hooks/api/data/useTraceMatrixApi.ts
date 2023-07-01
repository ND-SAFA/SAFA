import { defineStore } from "pinia";

import { TimArtifactLevelSchema } from "@/types";
import { useApi, typeOptionsStore, projectStore } from "@/hooks";
import { createTraceMatrix, deleteTraceMatrix } from "@/api";
import { pinia } from "@/plugins";

export const useTraceMatrixApi = defineStore("traceMatrixApi", () => {
  const traceMatrixApi = useApi("traceMatrixApi");

  /**
   * Creates traces from the given source to target artifact types.
   *
   * @param sourceArtifactTypeName - The source artifact type name.
   * @param targetArtifactTypeName - The target artifact type name.
   */
  async function handleCreate(
    sourceArtifactTypeName: string,
    targetArtifactTypeName: string
  ): Promise<void> {
    await traceMatrixApi.handleRequest(
      async () => {
        await createTraceMatrix(
          projectStore.projectId,
          sourceArtifactTypeName,
          targetArtifactTypeName
        );

        typeOptionsStore.updateLinkDirections({
          name: sourceArtifactTypeName,
          allowedTypes: [
            ...typeOptionsStore.tim.artifacts[sourceArtifactTypeName]
              .allowedTypes,
            targetArtifactTypeName,
          ],
        });
      },
      {},
      {
        success: `Created trace matrix: ${sourceArtifactTypeName} -> ${targetArtifactTypeName}`,
        error: `Unable to create trace matrix: ${sourceArtifactTypeName} -> ${targetArtifactTypeName}`,
      }
    );
  }

  /**
   * Removes traces from the given source to target artifact types.
   *
   * @param sourceArtifactTypeName - The source artifact type name.
   * @param targetArtifactTypeName - The target artifact type name.
   */
  async function handleDeleteTypes(
    sourceArtifactTypeName: string,
    targetArtifactTypeName: string
  ): Promise<void> {
    await traceMatrixApi.handleRequest(
      () =>
        deleteTraceMatrix(
          projectStore.projectId,
          sourceArtifactTypeName,
          targetArtifactTypeName
        ),
      {},
      {
        success: `Deleted trace matrix: ${sourceArtifactTypeName} -> ${targetArtifactTypeName}`,
        error: `Unable to delete trace matrix: ${sourceArtifactTypeName} -> ${targetArtifactTypeName}`,
      }
    );
  }

  /**
   Removes a type of traces from the given artifact level.
   *
   * @param artifactLevel - The artifact type to edit.
   * @param removedType - The type direction to remove.
   */
  async function handleDeleteDirection(
    artifactLevel: TimArtifactLevelSchema,
    removedType: string
  ): Promise<void> {
    artifactLevel.allowedTypes = artifactLevel.allowedTypes.filter(
      (allowedType) => allowedType !== removedType
    );

    typeOptionsStore.updateLinkDirections(artifactLevel);
    await handleDeleteTypes(artifactLevel.name, removedType);
  }

  return {
    handleCreate,
    handleDeleteTypes,
    handleDeleteDirection,
  };
});

export default useTraceMatrixApi(pinia);

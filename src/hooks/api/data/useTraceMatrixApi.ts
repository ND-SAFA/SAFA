import { defineStore } from "pinia";

import { useApi, projectStore, timStore } from "@/hooks";
import { createTraceMatrix, deleteTraceMatrix } from "@/api";
import { pinia } from "@/plugins";

export const useTraceMatrixApi = defineStore("traceMatrixApi", () => {
  const traceMatrixApi = useApi("traceMatrixApi");

  /**
   * Creates traces from the given source to target artifact types.
   *
   * @param sourceTypeName - The source artifact type name.
   * @param targetTypeName - The target artifact type name.
   */
  async function handleCreate(
    sourceTypeName: string,
    targetTypeName: string
  ): Promise<void> {
    await traceMatrixApi.handleRequest(
      async () => {
        await createTraceMatrix(
          projectStore.projectId,
          sourceTypeName,
          targetTypeName
        );

        timStore.addTraceMatrix(sourceTypeName, targetTypeName);
      },
      {},
      {
        success: `Created trace matrix: ${sourceTypeName} -> ${targetTypeName}`,
        error: `Unable to create trace matrix: ${sourceTypeName} -> ${targetTypeName}`,
      }
    );
  }

  /**
   * Removes traces from the given source to target artifact types.
   *
   * @param sourceTypeName - The source artifact type name.
   * @param targetTypeName - The target artifact type name.
   */
  async function handleDeleteTypes(
    sourceTypeName: string,
    targetTypeName: string
  ): Promise<void> {
    await traceMatrixApi.handleRequest(
      async () => {
        await deleteTraceMatrix(
          projectStore.projectId,
          sourceTypeName,
          targetTypeName
        );

        timStore.deleteTraceMatrix(sourceTypeName, targetTypeName);
      },
      {},
      {
        success: `Deleted trace matrix: ${sourceTypeName} -> ${targetTypeName}`,
        error: `Unable to delete trace matrix: ${sourceTypeName} -> ${targetTypeName}`,
      }
    );
  }

  return {
    handleCreate,
    handleDeleteTypes,
  };
});

export default useTraceMatrixApi(pinia);

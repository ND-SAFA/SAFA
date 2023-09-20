import { defineStore } from "pinia";

import { TraceMatrixApiHook } from "@/types";
import { useApi, projectStore, timStore } from "@/hooks";
import { createTraceMatrix, deleteTraceMatrix } from "@/api";
import { pinia } from "@/plugins";

/**
 * A hook for managing trace matrix API requests.
 */
export const useTraceMatrixApi = defineStore(
  "traceMatrixApi",
  (): TraceMatrixApiHook => {
    const traceMatrixApi = useApi("traceMatrixApi");

    async function handleCreate(
      sourceTypeName: string,
      targetTypeName: string
    ): Promise<void> {
      await traceMatrixApi.handleRequest(
        async () => {
          await createTraceMatrix(
            projectStore.versionId,
            sourceTypeName,
            targetTypeName
          );

          timStore.addTraceMatrix(sourceTypeName, targetTypeName);
        },
        {
          success: `Created trace matrix: ${sourceTypeName} -> ${targetTypeName}`,
          error: `Unable to create trace matrix: ${sourceTypeName} -> ${targetTypeName}`,
        }
      );
    }

    async function handleDeleteTypes(
      sourceTypeName: string,
      targetTypeName: string
    ): Promise<void> {
      await traceMatrixApi.handleRequest(
        async () => {
          await deleteTraceMatrix(
            projectStore.versionId,
            sourceTypeName,
            targetTypeName
          );

          timStore.deleteTraceMatrix(sourceTypeName, targetTypeName);
        },
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
  }
);

export default useTraceMatrixApi(pinia);

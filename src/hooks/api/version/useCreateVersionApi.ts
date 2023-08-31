import { defineStore } from "pinia";

import { computed } from "vue";
import {
  IOHandlerCallback,
  VersionSchema,
  VersionType,
  CreateVersionApiHook,
} from "@/types";
import { jobApiStore, useApi } from "@/hooks";
import { navigateTo, Routes } from "@/router";
import {
  createFlatFileUploadJob,
  createMajorVersion,
  createMinorVersion,
  createRevisionVersion,
} from "@/api";
import { pinia } from "@/plugins";

/**
 * A hook for managing create version API requests.
 */
export const useCreateVersionApi = defineStore(
  "createVersionApi",
  (): CreateVersionApiHook => {
    const createVersionApi = useApi("createVersionApi");

    const loading = computed(() => createVersionApi.loading);

    async function handleCreate(
      projectId: string,
      versionType: VersionType,
      callbacks: IOHandlerCallback<VersionSchema>
    ): Promise<void> {
      await createVersionApi.handleRequest(
        () => {
          if (versionType === "major") {
            return createMajorVersion(projectId);
          } else if (versionType === "minor") {
            return createMinorVersion(projectId);
          } else {
            return createRevisionVersion(projectId);
          }
        },
        {
          ...callbacks,
          useAppLoad: true,
          success: `Created a new version.`,
          error: "Unable to create a new version.",
        }
      );
    }

    async function handleImport(
      projectId: string,
      versionId: string,
      selectedFiles: File[],
      setVersionIfSuccessful: boolean,
      isCompleteSet = false
    ): Promise<void> {
      await createVersionApi.handleRequest(
        async () => {
          const formData = new FormData();

          selectedFiles.forEach((file: File) => {
            formData.append("files", file);
          });

          formData.append("isCompleteSet", JSON.stringify(isCompleteSet));

          const job = await createFlatFileUploadJob(versionId, formData);

          await jobApiStore.handleCreate(job);
        },
        {
          onComplete: async () => {
            if (!setVersionIfSuccessful) return;

            await navigateTo(Routes.UPLOAD_STATUS);
          },
          useAppLoad: true,
        }
      );
    }

    return {
      loading,
      handleReset: () => createVersionApi.handleReset(),
      handleCreate,
      handleImport,
    };
  }
);

export default useCreateVersionApi(pinia);

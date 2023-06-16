import { defineStore } from "pinia";

import { computed } from "vue";
import { IOHandlerCallback, VersionSchema, VersionType } from "@/types";
import { jobApiStore, useApi } from "@/hooks";
import { navigateTo, Routes } from "@/router";
import {
  createFlatFileUploadJob,
  createMajorVersion,
  createMinorVersion,
  createRevisionVersion,
} from "@/api";
import { pinia } from "@/plugins";

export const useCreateVersionApi = defineStore("createVersionApi", () => {
  const createVersionApi = useApi("createVersionApi");

  const loading = computed(() => createVersionApi.loading);

  /**
   * Creates a new version.
   *
   * @param projectId - The project to create a version for.
   * @param versionType - The version type to create.
   * @param callbacks - The callbacks to use on success, error, and complete.
   */
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
      callbacks,
      {
        useAppLoad: true,
        success: `Created a new version.`,
        error: "Unable to create a new version.",
      }
    );
  }

  /**
   * Creates a new version for a project, uploading the files related to it.
   *
   * @param projectId - The project that has been selected by the user.
   * @param versionId - The version associated with given project to update.
   * @param selectedFiles  - The flat files that will update given version.
   * @param setVersionIfSuccessful - Whether the store should be set to the uploaded version if successful.
   * @param isCompleteSet - Whether to delete any other artifacts in the current version.
   */
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
      },
      { useAppLoad: true }
    );
  }

  return {
    loading,
    handleReset: () => createVersionApi.handleReset(),
    handleCreate,
    handleImport,
  };
});

export default useCreateVersionApi(pinia);

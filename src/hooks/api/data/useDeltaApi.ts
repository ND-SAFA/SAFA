import { defineStore } from "pinia";

import { computed } from "vue";
import { DeltaApiHook, IOHandlerCallback, VersionSchema } from "@/types";
import {
  useApi,
  deltaStore,
  projectStore,
  getVersionApiStore,
  documentStore,
} from "@/hooks";
import { getProjectDelta } from "@/api";
import { pinia } from "@/plugins";

/**
 * A hook for managing delta API requests.
 */
export const useDeltaApi = defineStore("deltaApi", (): DeltaApiHook => {
  const deltaApi = useApi("deltaApi");

  const loading = computed(() => deltaApi.loading);

  const deltaVersions = computed(() => {
    const currentVersionId = projectStore.version?.versionId;

    return projectStore.allVersions.filter(
      ({ versionId }) => versionId !== currentVersionId
    );
  });

  async function handleCreate(
    targetVersion?: VersionSchema,
    callbacks: IOHandlerCallback = {}
  ): Promise<void> {
    await deltaApi.handleRequest(
      async () => {
        if (!targetVersion || !projectStore.version) return;

        const delta = await getProjectDelta(
          projectStore.version.versionId,
          targetVersion.versionId
        );

        await deltaStore.setDeltaPayload(delta, targetVersion);
      },
      {
        ...callbacks,
        success: "Delta state was updated successfully.",
        error: "Unable to set delta state.",
      }
    );
  }

  async function handleDisable(): Promise<void> {
    deltaStore.setIsDeltaViewEnabled(false);
    await getVersionApiStore.handleLoad(
      projectStore.versionId,
      documentStore.currentDocument.documentId
    );
  }

  return { loading, deltaVersions, handleCreate, handleDisable };
});

export default useDeltaApi(pinia);

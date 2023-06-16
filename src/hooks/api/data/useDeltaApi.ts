import { defineStore } from "pinia";

import { computed } from "vue";
import { IOHandlerCallback, VersionSchema } from "@/types";
import { useApi, deltaStore, projectStore, getVersionApiStore } from "@/hooks";
import { getProjectDelta } from "@/api";
import { pinia } from "@/plugins";

export const useDeltaApi = defineStore("deltaApi", () => {
  const deltaApi = useApi("deltaApi");

  const loading = computed(() => deltaApi.loading);

  const deltaVersions = computed(() => {
    const currentVersionId = projectStore.version?.versionId;

    return getVersionApiStore.allVersions.filter(
      ({ versionId }) => versionId !== currentVersionId
    );
  });

  /**
   * Sets a project delta.
   *
   * @param targetVersion - The target version of the project.
   * @param callbacks - Callbacks for the request.
   */
  async function handleSetProjectDelta(
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
      callbacks,
      {
        success: "Delta state was updated successfully.",
        error: "Unable to set delta state.",
      }
    );
  }

  return { loading, deltaVersions, handleSetProjectDelta };
});

export default useDeltaApi(pinia);

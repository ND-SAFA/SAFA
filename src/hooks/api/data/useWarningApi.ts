import { defineStore } from "pinia";

import { useApi, warningStore } from "@/hooks";
import { getWarningsInProjectVersion } from "@/api";
import { pinia } from "@/plugins";

export const useWarningApi = defineStore("warningApi", () => {
  const warningApi = useApi("warningApi");

  /**
   * Call this function whenever warnings need to be re-downloaded.
   *
   * @param versionId - The project version to load from.
   */
  async function handleReload(versionId: string): Promise<void> {
    await warningApi.handleRequest(async () => {
      warningStore.artifactWarnings = await getWarningsInProjectVersion(
        versionId
      );
    });
  }

  return { handleReload };
});

export default useWarningApi(pinia);

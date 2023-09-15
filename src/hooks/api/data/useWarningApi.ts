import { defineStore } from "pinia";

import { WarningApiHook } from "@/types";
import { useApi, warningStore } from "@/hooks";
import { getWarningsInProjectVersion } from "@/api";
import { pinia } from "@/plugins";

/**
 * A hook for managing warning API requests.
 */
export const useWarningApi = defineStore("warningApi", (): WarningApiHook => {
  const warningApi = useApi("warningApi");

  async function handleReload(versionId: string): Promise<void> {
    await warningApi.handleRequest(async () => {
      warningStore.artifactWarnings =
        await getWarningsInProjectVersion(versionId);
    });
  }

  return { handleReload };
});

export default useWarningApi(pinia);

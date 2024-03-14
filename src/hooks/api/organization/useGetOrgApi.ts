import { defineStore } from "pinia";
import { computed } from "vue";

import { GetOrgApiHook } from "@/types";
import { orgStore, sessionStore, useApi } from "@/hooks";
import { getOrganizations, getPersonalOrganization } from "@/api";
import { pinia } from "@/plugins";

/**
 * A hook for managing requests to the get organizations API.
 */
export const useGetOrgApi = defineStore("getOrgApi", (): GetOrgApiHook => {
  const getOrgApi = useApi("getOrgApi");

  const loading = computed(() => getOrgApi.loading);

  async function handleLoadCurrent(): Promise<void> {
    if (!sessionStore.doesSessionExist) return;

    await getOrgApi.handleRequest(
      async () => {
        orgStore.allOrgs = await getOrganizations();

        orgStore.org = (await getPersonalOrganization()) || orgStore.allOrgs[0];
      },
      {
        error: "Unable to load your current organization.",
      }
    );
  }

  return {
    loading,
    handleLoadCurrent,
  };
});

export default useGetOrgApi(pinia);

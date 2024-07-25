import { defineStore } from "pinia";
import { computed } from "vue";

import { GetOrgApiHook } from "@/types";
import { orgApiStore, orgStore, useApi } from "@/hooks";
import { getOrganizations, getPersonalOrganization } from "@/api";
import { pinia } from "@/plugins";

/**
 * A hook for managing requests to the get organizations API.
 */
export const useGetOrgApi = defineStore("getOrgApi", (): GetOrgApiHook => {
  const getOrgApi = useApi("getOrgApi");

  const loading = computed(() => getOrgApi.loading);

  async function handleLoad(orgId: string): Promise<void> {
    await getOrgApi.handleRequest(
      async () => {
        orgStore.allOrgs = await getOrganizations();
        orgApiStore.currentOrg =
          orgStore.allOrgs.find((org) => org.id === orgId) ||
          orgStore.allOrgs[0];
      },
      {
        error: "Unable to load organization.",
      }
    );
  }

  async function handleLoadCurrent(): Promise<void> {
    await getOrgApi.handleRequest(
      async () => {
        orgStore.allOrgs = await getOrganizations();
        orgApiStore.currentOrg =
          (await getPersonalOrganization()) || orgStore.allOrgs[0];
      },
      {
        error: "Unable to load your current organization.",
      }
    );
  }

  return {
    loading,
    handleLoad,
    handleLoadCurrent,
  };
});

export default useGetOrgApi(pinia);

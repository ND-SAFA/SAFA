import { defineStore } from "pinia";
import { computed } from "vue";

import { GetOrgApiHook, OrganizationSchema } from "@/types";
import { orgStore, sessionStore, useApi } from "@/hooks";
import { getOrganization, getOrganizations, saveDefaultOrg } from "@/api";
import { pinia } from "@/plugins";

/**
 * A hook for managing requests to the get organizations API.
 */
export const useGetOrgApi = defineStore("getOrgApi", (): GetOrgApiHook => {
  const getOrgApi = useApi("getOrgApi");

  const loading = computed(() => getOrgApi.loading);

  async function handleSwitch(org: OrganizationSchema): Promise<void> {
    orgStore.org = org;

    await saveDefaultOrg(org.id);
  }

  async function handleLoadCurrent(): Promise<void> {
    if (!sessionStore.doesSessionExist) return;

    await getOrgApi.handleRequest(
      async () => {
        orgStore.allOrgs = await getOrganizations();

        const orgId = sessionStore.user.defaultOrgId || orgStore.allOrgs[0]?.id;

        if (!orgId) return;

        orgStore.org = await getOrganization(orgId);
      },
      {
        error: "Unable to load your current organization.",
      }
    );
  }

  return {
    loading,
    handleSwitch,
    handleLoadCurrent,
  };
});

export default useGetOrgApi(pinia);

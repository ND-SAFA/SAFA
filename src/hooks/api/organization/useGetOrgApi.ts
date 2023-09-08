import { defineStore } from "pinia";
import { ref, computed } from "vue";

import { GetOrgApiHook, OrganizationSchema } from "@/types";
import { removeMatches } from "@/util";
import { orgStore, sessionStore, useApi } from "@/hooks";
import { getOrganization, getOrganizations, saveDefaultOrg } from "@/api";
import { pinia } from "@/plugins";

/**
 * A hook for managing requests to the get organizations API.
 */
export const useGetOrgApi = defineStore("getOrgApi", (): GetOrgApiHook => {
  const getOrgApi = useApi("getOrgApi");

  const allOrgs = ref<OrganizationSchema[]>([]);

  const unloadedOrgs = computed(() =>
    allOrgs.value.filter(({ id }) => id !== orgStore.orgId)
  );

  const loading = computed(() => getOrgApi.loading);

  function addOrg(org: OrganizationSchema): void {
    allOrgs.value = [org, ...removeMatches(allOrgs.value, "id", [org.id])];
  }

  function removeOrg(org: OrganizationSchema): void {
    allOrgs.value = allOrgs.value.filter(({ id }) => id !== org.id);
  }

  async function handleSwitch(org: OrganizationSchema): Promise<void> {
    orgStore.org = org;

    await saveDefaultOrg(org.id);
  }

  async function handleLoadCurrent(): Promise<void> {
    if (!sessionStore.doesSessionExist) return;

    await getOrgApi.handleRequest(
      async () => {
        allOrgs.value = await getOrganizations();

        const orgId = sessionStore.user.defaultOrgId || allOrgs.value[0]?.id;

        if (!orgId) return;

        orgStore.org = await getOrganization(orgId);
      },
      {
        error: "Unable to load your current organization.",
      }
    );
  }

  return {
    allOrgs,
    unloadedOrgs,
    loading,
    addOrg,
    removeOrg,
    handleSwitch,
    handleLoadCurrent,
  };
});

export default useGetOrgApi(pinia);

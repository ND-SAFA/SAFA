import { defineStore } from "pinia";
import { ref } from "vue";

import { computed } from "vue/dist/vue";
import { GetOrgApiHook, IOHandlerCallback, OrganizationSchema } from "@/types";
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

  const currentOrg = computed({
    get: () => (orgStore.orgId ? orgStore.org : undefined),
    set(org: OrganizationSchema | undefined) {
      if (!org) return;

      orgStore.org = org;

      saveDefaultOrg(org.id);
    },
  });

  function addOrg(org: OrganizationSchema): void {
    allOrgs.value = [org, ...removeMatches(allOrgs.value, "id", [org.id])];
  }

  function removeOrg(org: OrganizationSchema): void {
    allOrgs.value = allOrgs.value.filter(({ id }) => id !== org.id);
  }

  async function handleReload(
    callbacks: IOHandlerCallback = {}
  ): Promise<void> {
    if (!sessionStore.doesSessionExist) {
      callbacks.onSuccess?.();
      return;
    }

    await getOrgApi.handleRequest(
      async () => {
        allOrgs.value = await getOrganizations();
      },
      {
        ...callbacks,
        error: "Unable to load your organizations.",
      }
    );
  }

  async function handleLoadCurrent(): Promise<void> {
    const orgId = sessionStore.user.defaultOrgId;

    if (!sessionStore.doesSessionExist || !orgId) return;

    await getOrgApi.handleRequest(
      async () => {
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
    currentOrg,
    addOrg,
    removeOrg,
    handleReload,
    handleLoadCurrent,
  };
});

export default useGetOrgApi(pinia);

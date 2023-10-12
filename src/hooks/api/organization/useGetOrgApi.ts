import { defineStore } from "pinia";
import { computed } from "vue";

import { GetOrgApiHook, OrganizationSchema } from "@/types";
import { orgStore, sessionStore, teamStore, useApi } from "@/hooks";
import {
  getOrganizations,
  getPersonalOrganization,
  saveDefaultOrg,
} from "@/api";
import { pinia } from "@/plugins";

/**
 * A hook for managing requests to the get organizations API.
 */
export const useGetOrgApi = defineStore("getOrgApi", (): GetOrgApiHook => {
  const getOrgApi = useApi("getOrgApi");

  const loading = computed(() => getOrgApi.loading);

  const currentOrg = computed({
    get: () => orgStore.org,
    set(org: OrganizationSchema | undefined) {
      handleSwitch(org);
    },
  });

  async function handleSwitch(
    org: OrganizationSchema | undefined
  ): Promise<void> {
    if (!org) return;

    saveDefaultOrg(org.id);

    orgStore.org = org;
    teamStore.team =
      orgStore.org.teams?.find(({ members = [] }) =>
        members.find(({ email }) => email === sessionStore.userEmail)
      ) || teamStore.team;
  }

  async function handleLoadCurrent(): Promise<void> {
    if (!sessionStore.doesSessionExist) return;

    await getOrgApi.handleRequest(
      async () => {
        orgStore.allOrgs = await getOrganizations();

        currentOrg.value =
          (await getPersonalOrganization()) || orgStore.allOrgs[0];
      },
      {
        error: "Unable to load your current organization.",
      }
    );
  }

  return {
    loading,
    currentOrg,
    handleSwitch,
    handleLoadCurrent,
  };
});

export default useGetOrgApi(pinia);

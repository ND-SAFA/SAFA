import { defineStore } from "pinia";

import { computed } from "vue";
import { IOHandlerCallback, OrganizationSchema, OrgApiHook } from "@/types";
import { getOrgApiStore, logStore, orgStore, useApi } from "@/hooks";
import {
  createOrganization,
  deleteOrganization,
  editOrganization,
} from "@/api";
import { pinia } from "@/plugins";

/**
 * A hook for managing requests to the organizations API.
 */
export const useOrgApi = defineStore("orgApi", (): OrgApiHook => {
  const saveOrgApi = useApi("saveOrgApi");
  const deleteOrgApi = useApi("deleteOrgApi");

  const saveOrgApiLoading = computed(() => saveOrgApi.loading);
  const deleteOrgApiLoading = computed(() => deleteOrgApi.loading);

  async function handleSave(
    org: OrganizationSchema,
    callbacks: IOHandlerCallback = {}
  ): Promise<void> {
    await saveOrgApi.handleRequest(
      async () => {
        if (!org.id) {
          const createdOrg = await createOrganization(org);

          getOrgApiStore.addOrg(createdOrg);
          orgStore.org = createdOrg;
        } else {
          const editedOrg = await editOrganization(org);

          getOrgApiStore.addOrg(editedOrg);
          orgStore.org = editedOrg;
        }
      },
      {
        ...callbacks,
        success: `Organization has been saved: ${org.name}`,
        error: `Unable to save organization: ${org.name}`,
      }
    );
  }

  async function handleDelete(
    callbacks: IOHandlerCallback = {}
  ): Promise<void> {
    const org = orgStore.org;

    logStore.confirm(
      "Delete Organization",
      `Are you sure you want to delete ${org.name}?`,
      async (isConfirmed) => {
        if (!isConfirmed) return;

        await deleteOrgApi.handleRequest(
          async () => {
            await deleteOrganization(org);

            getOrgApiStore.removeOrg(org);

            if (orgStore.orgId !== org.id) return;

            // Clear the current org if it was deleted.
            orgStore.$reset();
          },
          {
            ...callbacks,
            success: `Organization has been deleted: ${org.name}`,
            error: `Unable to delete organization: ${org.name}`,
          }
        );
      }
    );
  }

  return {
    saveOrgApiLoading,
    deleteOrgApiLoading,
    handleSave,
    handleDelete,
  };
});

export default useOrgApi(pinia);

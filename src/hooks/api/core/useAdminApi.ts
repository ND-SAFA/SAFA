import { defineStore } from "pinia";

import { computed } from "vue";
import {
  AdminApiHook,
  MembershipSchema,
  OrganizationSchema,
  OrgPaymentTier,
} from "@/types";
import { logStore, sessionStore } from "@/hooks";
import {
  activateSuperuser,
  createSuperuser,
  deactivateSuperuser,
  setOrgPaymentTier,
} from "@/api";
import { pinia } from "@/plugins";
import useApi from "./useApi";

/**
 * This API store manages the current user's superuser status, allowing SAFA admins
 * to overrule permission checks.
 */
export const useAdminApi = defineStore("useAdmin", (): AdminApiHook => {
  const adminApi = useApi("adminApi");

  const activeSuperuser = computed({
    get() {
      return sessionStore.user?.admin?.active || false;
    },
    set(active: boolean) {
      adminApi.handleRequest(
        async () => {
          if (active) {
            await activateSuperuser();
          } else {
            await deactivateSuperuser();
          }

          sessionStore.updateUser({ admin: { active } });
        },
        {
          success: active
            ? "Superuser powers activated."
            : "Superuser powers deactivated.",
          error: active
            ? "Failed to activate superuser powers."
            : "Failed to deactivate superuser powers.",
        }
      );
    },
  });

  async function enableSuperuser(
    member: Pick<MembershipSchema, "email">
  ): Promise<void> {
    logStore.confirm(
      "Enable Superuser",
      `Are you sure you want to enable superuser for "${member.email}"?`,
      async (confirmed) => {
        if (!confirmed) return;

        await adminApi.handleRequest(() => createSuperuser(member.email), {
          success: `User is now a superuser: ${member.email}`,
          error: `Unable to set as a superuser: ${member.email}`,
        });
      }
    );
  }

  async function updatePaymentTier(
    org: OrganizationSchema,
    tier: OrgPaymentTier
  ): Promise<void> {
    logStore.confirm(
      "Enable Superuser",
      `Are you sure you want to set "${org.name}" as "${tier}"?`,
      async (confirmed) => {
        if (!confirmed) return;

        await adminApi.handleRequest(() => setOrgPaymentTier(org.id, tier), {
          success: `Org is now set to "${tier}": ${org.name}`,
          error: `Unable to set org as "${tier}": ${org.name}`,
        });
      }
    );
  }

  return { activeSuperuser, enableSuperuser, updatePaymentTier };
});

export default useAdminApi(pinia);
